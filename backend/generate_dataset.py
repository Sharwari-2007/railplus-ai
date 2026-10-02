import os
import math
import random
from datetime import datetime, timedelta
import openpyxl

def generate_weather_dataset():
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    os.makedirs(data_dir, exist_ok=True)
    filepath = os.path.join(data_dir, "india_weather_rainfall_data.xlsx")

    # Major Indian Railway Stations / Junctions with real GIS coordinates
    stations = [
        {"name": "New Delhi", "state": "Delhi", "district": "Central Delhi", "lat": 28.6139, "lon": 77.2090, "elev": 216},
        {"name": "Agra Cantt", "state": "Uttar Pradesh", "district": "Agra", "lat": 27.1577, "lon": 78.0076, "elev": 169},
        {"name": "Gwalior Junction", "state": "Madhya Pradesh", "district": "Gwalior", "lat": 26.2183, "lon": 78.1828, "elev": 211},
        {"name": "VGL Jhansi", "state": "Uttar Pradesh", "district": "Jhansi", "lat": 25.4484, "lon": 78.5685, "elev": 285},
        {"name": "Bhopal Junction", "state": "Madhya Pradesh", "district": "Bhopal", "lat": 23.2599, "lon": 77.4126, "elev": 527},
        {"name": "Itarsi Junction", "state": "Madhya Pradesh", "district": "Hoshangabad", "lat": 22.6114, "lon": 77.7656, "elev": 304},
        {"name": "Nagpur Junction", "state": "Maharashtra", "district": "Nagpur", "lat": 21.1458, "lon": 79.0882, "elev": 310},
        {"name": "Balharshah", "state": "Maharashtra", "district": "Chandrapur", "lat": 19.8540, "lon": 79.3414, "elev": 185},
        {"name": "Vijayawada Junction", "state": "Andhra Pradesh", "district": "Krishna", "lat": 16.5062, "lon": 80.6480, "elev": 23},
        {"name": "Chennai Central", "state": "Tamil Nadu", "district": "Chennai", "lat": 13.0827, "lon": 80.2707, "elev": 6},
        {"name": "Mumbai Central", "state": "Maharashtra", "district": "Mumbai City", "lat": 18.9696, "lon": 72.8193, "elev": 10},
        {"name": "Surat", "state": "Gujarat", "district": "Surat", "lat": 21.1702, "lon": 72.8311, "elev": 13},
        {"name": "Vadodara Junction", "state": "Gujarat", "district": "Vadodara", "lat": 22.3072, "lon": 73.1812, "elev": 39},
        {"name": "Ahmedabad Junction", "state": "Gujarat", "district": "Ahmedabad", "lat": 23.0225, "lon": 72.5714, "elev": 53},
        {"name": "Kanpur Central", "state": "Uttar Pradesh", "district": "Kanpur", "lat": 26.4499, "lon": 80.3319, "elev": 126},
        {"name": "Prayagraj Junction", "state": "Uttar Pradesh", "district": "Prayagraj", "lat": 25.4358, "lon": 81.8463, "elev": 98},
        {"name": "Varanasi Junction", "state": "Uttar Pradesh", "district": "Varanasi", "lat": 25.3176, "lon": 82.9739, "elev": 81},
        {"name": "Pandit Deen Dayal Upadhyaya", "state": "Uttar Pradesh", "district": "Chandauli", "lat": 25.2818, "lon": 83.1189, "elev": 78},
        {"name": "Howrah Junction", "state": "West Bengal", "district": "Howrah", "lat": 22.5858, "lon": 88.3426, "elev": 12},
        {"name": "Pune Junction", "state": "Maharashtra", "district": "Pune", "lat": 18.5204, "lon": 73.8567, "elev": 560},
        {"name": "Kolkata Sealdah", "state": "West Bengal", "district": "Kolkata", "lat": 22.5670, "lon": 88.3712, "elev": 11},
        {"name": "Bengaluru City", "state": "Karnataka", "district": "Bengaluru", "lat": 12.9778, "lon": 77.5707, "elev": 920},
    ]

    start_date = datetime(2025, 1, 1)
    random.seed(42)

    month_names = ["January", "February", "March", "April", "May", "June", 
                   "July", "August", "September", "October", "November", "December"]

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Weather_Data"

    headers = [
        "date_of_record", "month", "season", "station_name", "state", "district",
        "avg_temp", "min_temp", "max_temp", "wind_speed", "air_pressure", "elevation",
        "latitude", "longitude", "rainfall"
    ]
    ws.append(headers)

    # Generate 365 days of weather records
    for d in range(365):
        current_date = start_date + timedelta(days=d)
        m = current_date.month
        month_str = month_names[m - 1]

        if m in [6, 7, 8, 9]:
            season = "Monsoon"
        elif m in [12, 1, 2]:
            season = "Winter"
        elif m in [3, 4, 5]:
            season = "Summer"
        else:
            season = "Post-Monsoon"

        for st in stations:
            if season == "Winter":
                base_min = random.gauss(5.0 if "Delhi" in st["name"] or "Agra" in st["name"] or "Jhansi" in st["name"] else 12.0, 2.0)
                base_max = base_min + random.uniform(10.0, 16.0)
                base_avg = (base_min + base_max) / 2.0
                air_press = random.gauss(1020.0, 2.0)
                rainfall = random.expovariate(0.5) if random.random() < 0.15 else 0.0
                wind = random.gauss(12.0, 3.0)
            elif season == "Monsoon":
                base_min = random.gauss(24.0, 1.5)
                base_max = random.gauss(32.0, 2.0)
                base_avg = (base_min + base_max) / 2.0
                air_press = random.gauss(1004.0, 3.0)
                if random.random() < 0.65:
                    if random.random() < 0.25:
                        rainfall = random.uniform(55.0, 135.0)
                    else:
                        rainfall = random.uniform(10.0, 48.0)
                else:
                    rainfall = 0.0
                wind = random.gauss(28.0, 6.0)
            elif season == "Summer":
                base_min = random.gauss(26.0, 2.0)
                base_max = random.gauss(42.0, 2.0)
                base_avg = (base_min + base_max) / 2.0
                air_press = random.gauss(1008.0, 2.5)
                rainfall = random.expovariate(0.3) if random.random() < 0.10 else 0.0
                wind = random.gauss(18.0, 4.0) if random.random() > 0.1 else random.uniform(46.0, 62.0)
            else:
                base_min = random.gauss(18.0, 2.0)
                base_max = random.gauss(30.0, 2.0)
                base_avg = (base_min + base_max) / 2.0
                air_press = random.gauss(1014.0, 2.0)
                rainfall = random.expovariate(0.2) if random.random() < 0.20 else 0.0
                wind = random.gauss(15.0, 4.0)

            ws.append([
                current_date.strftime("%Y-%m-%d"),
                month_str,
                season,
                st["name"],
                st["state"],
                st["district"],
                round(base_avg, 1),
                round(base_min, 1),
                round(base_max, 1),
                max(2.0, round(wind, 1)),
                round(air_press, 1),
                st["elev"],
                st["lat"],
                st["lon"],
                max(0.0, round(rainfall, 1))
            ])

    wb.save(filepath)
    print(f"Successfully generated weather dataset at {filepath}")

if __name__ == "__main__":
    generate_weather_dataset()
