from fastapi import APIRouter, Query
from data_loader import weather_loader

router = APIRouter(prefix="/api/weather", tags=["Weather Integration"])

@router.get("/historic-days")
def get_historic_days():
    """List sample historic weather days for corridor stress-testing"""
    return weather_loader.get_historic_days()

@router.get("/node")
def get_weather_for_node(
    lat: float = Query(27.1577, description="Latitude"),
    lon: float = Query(78.0076, description="Longitude"),
    date_str: str = Query("2025-07-15", description="Date YYYY-MM-DD")
):
    """Weather Proximity Index: Haversine/KDTree nearest weather station lookup"""
    return weather_loader.get_weather_for_node(lat, lon, date_str)

@router.get("/stations")
def get_all_weather_stations(date_str: str = Query("2025-07-15")):
    """Returns all weather stations and rain/fog intensity for GIS radar layer overlay"""
    records = []
    for st_name in weather_loader.unique_stations:
        coords = weather_loader.station_coords[st_name]
        w_data = weather_loader.get_weather_for_node(coords["lat"], coords["lon"], date_str)
        records.append({
            "station_name": st_name,
            "lat": coords["lat"],
            "lon": coords["lon"],
            "rainfall_mm": w_data.get("rainfall", 0.0),
            "min_temp": w_data.get("min_temp", 20.0),
            "wind_speed": w_data.get("wind_speed", 15.0),
            "air_pressure": w_data.get("air_pressure", 1012.0),
            "season": w_data.get("season", "Monsoon")
        })
    return records
