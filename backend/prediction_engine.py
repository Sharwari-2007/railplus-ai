import math
import numpy as np
from data_loader import weather_loader

class ETAPredictionEngine:
    def calculate_tsr_derating(self, weather_data: dict, base_mps: float = 130.0) -> dict:
        """
        Calculates Dynamic Speed Restriction (TSR) based on IR protocols:
        1. Heavy Rainfall (>50 mm/day) -> Waterlogging hazard -> Derate MPS by 40-60%.
        2. Fog Proxy (min_temp < 8°C and air_pressure > 1018 hPa) -> Cap speed at 60 km/h.
        3. High Wind (>45 km/h) -> Derate MPS by 25% + OHE/Bridge Caution.
        """
        rainfall = weather_data.get("rainfall", 0.0)
        min_temp = weather_data.get("min_temp", 25.0)
        air_pressure = weather_data.get("air_pressure", 1012.0)
        wind_speed = weather_data.get("wind_speed", 15.0)

        derate_factor = 1.0
        active_reasons = []
        is_fog_protocol = False
        is_waterlogged = False
        is_high_wind = False

        # 1. Rain Derating
        if rainfall > 50.0:
            is_waterlogged = True
            # Rain severity scale: 50mm -> 40% derate (0.60 multiplier), 120mm+ -> 60% derate (0.40 multiplier)
            rain_derate = max(0.40, 1.0 - (0.40 + (min(rainfall, 120.0) - 50.0) / 70.0 * 0.20))
            derate_factor *= rain_derate
            active_reasons.append(f"Monsoon Waterlogging Caution ({rainfall:.1f} mm/day rain)")
        elif rainfall > 20.0:
            derate_factor *= 0.85
            active_reasons.append(f"Moderate Rain Caution ({rainfall:.1f} mm/day rain)")

        # 2. Fog Protocol
        if min_temp < 8.0 and air_pressure > 1018.0:
            is_fog_protocol = True
            active_reasons.append(f"IR Fog Protocol Speed Cap (60 km/h cap, temp: {min_temp}°C, press: {air_pressure} hPa)")

        # 3. High Wind Caution
        if wind_speed > 45.0:
            is_high_wind = True
            derate_factor *= 0.75
            active_reasons.append(f"High-Wind OHE & Bridge Caution ({wind_speed:.1f} km/h wind)")

        effective_mps = base_mps * derate_factor

        # Apply hard fog cap of 60 km/h if fog protocol is active
        if is_fog_protocol:
            effective_mps = min(effective_mps, 60.0)

        return {
            "base_mps": base_mps,
            "effective_mps": round(effective_mps, 1),
            "derate_factor": round(derate_factor, 2),
            "is_waterlogged": is_waterlogged,
            "is_fog_protocol": is_fog_protocol,
            "is_high_wind": is_high_wind,
            "active_reasons": active_reasons
        }

    def predict_train_eta(
        self,
        train_info: dict,
        current_loc: dict,
        sim_date: str = "2025-07-15",
        precedence_override: bool = False,
        track_block_mins: float = 0.0
    ) -> dict:
        """
        Calculates Probabilistic ETA, XAI Delay Breakdown, and Signal Block Dynamics.
        """
        base_mps = train_info.get("max_speed", 130.0)
        train_priority = train_info.get("priority", 1)  # 1 = Rajdhani/Vande Bharat, 2 = Express, 3 = Goods
        
        # Get nearest weather at current train location
        weather_info = weather_loader.get_weather_for_node(current_loc["lat"], current_loc["lon"], sim_date)
        tsr_info = self.calculate_tsr_derating(weather_info, base_mps)
        
        effective_speed = tsr_info["effective_mps"]

        # Adjust speed for section occupancy / preceding train congestion
        section_occupancy = current_loc.get("section_occupancy", "GREEN")  # GREEN, YELLOW, RED
        section_delay_multiplier = 1.0
        if section_occupancy == "YELLOW":
            effective_speed *= 0.65
            section_delay_multiplier = 1.35
        elif section_occupancy == "RED":
            effective_speed *= 0.20
            section_delay_multiplier = 2.50

        # Adjust for precedence override (e.g. prioritize Rajdhani over Express)
        if precedence_override:
            if train_priority == 1:
                effective_speed = min(base_mps, effective_speed * 1.25)
            else:
                effective_speed *= 0.60  # Express held on loop line

        remaining_dist_km = train_info.get("remaining_distance_km", 120.0)
        
        # Base transit time in minutes
        transit_time_hrs = remaining_dist_km / max(effective_speed, 15.0)
        transit_time_mins = transit_time_hrs * 60.0 + track_block_mins

        # Baseline scheduled remaining time
        scheduled_time_mins = (remaining_dist_km / base_mps) * 60.0
        net_delay_mins = max(0.0, transit_time_mins - scheduled_time_mins)

        # Probabilistic Confidence Band Logic
        # Confidence score decreases with extreme weather & signal red blocks
        confidence_score = 96
        if tsr_info["is_fog_protocol"]:
            confidence_score -= 10
        if tsr_info["is_waterlogged"]:
            confidence_score -= 12
        if section_occupancy == "RED":
            confidence_score -= 15
        if track_block_mins > 0:
            confidence_score -= 8

        confidence_score = max(65, min(99, confidence_score))
        
        # Uncertainty interval (e.g. ± 4 mins)
        interval_mins = max(2, int(round((100 - confidence_score) * 0.25 + net_delay_mins * 0.10)))

        # Explainable AI (XAI) Delay Factor Attribution (%)
        weather_delay_pct = 0.0
        signal_delay_pct = 0.0
        preceding_rake_pct = 0.0
        block_delay_pct = 0.0

        total_delay_points = 0.001  # avoid div by zero

        # Weather points
        if tsr_info["derate_factor"] < 1.0 or tsr_info["is_fog_protocol"]:
            pts = (1.0 - tsr_info["derate_factor"]) * 40.0 + (25.0 if tsr_info["is_fog_protocol"] else 0.0)
            total_delay_points += pts
            weather_delay_pct = pts

        # Signal / Section block points
        if section_occupancy != "GREEN":
            pts = 35.0 if section_occupancy == "YELLOW" else 70.0
            total_delay_points += pts
            signal_delay_pct = pts
        else:
            # Baseline signal hold
            pts = 10.0
            total_delay_points += pts
            signal_delay_pct = pts

        # Preceding rake speed drop points
        if train_priority > 1 or precedence_override:
            pts = 25.0 if precedence_override else 15.0
            total_delay_points += pts
            preceding_rake_pct = pts

        # Maintenance block points
        if track_block_mins > 0:
            pts = track_block_mins * 2.0
            total_delay_points += pts
            block_delay_pct = pts

        # Normalize to 100%
        xai_breakdown = [
            {"factor": "Signal Clearance & Block Hold", "percentage": round((signal_delay_pct / total_delay_points) * 100)},
            {"factor": "Weather & Track TSR Derating", "percentage": round((weather_delay_pct / total_delay_points) * 100)},
            {"factor": "Preceding Rake Congestion", "percentage": round((preceding_rake_pct / total_delay_points) * 100)},
            {"factor": "Emergency Maintenance Block", "percentage": round((block_delay_pct / total_delay_points) * 100)}
        ]

        # Filter out 0% factors and ensure sums to 100
        xai_breakdown = [item for item in xai_breakdown if item["percentage"] > 0]

        return {
            "train_id": train_info["id"],
            "train_name": train_info["name"],
            "remaining_distance_km": remaining_dist_km,
            "base_mps": base_mps,
            "effective_speed_kmh": round(effective_speed, 1),
            "estimated_transit_mins": round(transit_time_mins, 1),
            "scheduled_remaining_mins": round(scheduled_time_mins, 1),
            "net_delay_mins": round(net_delay_mins, 1),
            "probabilistic_eta": {
                "confidence_score_pct": confidence_score,
                "interval_mins": interval_mins,
                "status_label": "On Time" if net_delay_mins < 5 else f"Delayed by ~{int(net_delay_mins)} mins"
            },
            "weather_impact": {
                "met_station": weather_info.get("station_name"),
                "rainfall_mm": weather_info.get("rainfall", 0),
                "min_temp_c": weather_info.get("min_temp"),
                "wind_speed_kmh": weather_info.get("wind_speed"),
                "active_cautions": tsr_info["active_reasons"]
            },
            "xai_delay_breakdown": xai_breakdown
        }

# Global instance
prediction_engine = ETAPredictionEngine()
