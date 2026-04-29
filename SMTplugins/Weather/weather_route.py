from flask import Blueprint, jsonify, request
import requests
from geopy.geocoders import Nominatim
import os
import json

weather_bp = Blueprint('weather_bp', __name__)
geolocator = Nominatim(user_agent="SMT_Terminal_Project")

# NWS requires a unique User-Agent header
HEADERS = {
    'User-Agent': '(SMT-Project, bschadoff@albany.edu)',
    'Accept': 'application/geo+json'
}

DATA_FILE = "SMTplugins/Weather/weather_city.json"


@weather_bp.route('/api/weather/smt', methods=['GET'])
def get_nws_weather():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                currentVal = str(data.get("city"))
        except Exception as e:
            print(f"Error reading JSON File: {e}")

    city = request.args.get('city', currentVal)
    try:
        # 1) Geocode city to Lat/Lon
        location = geolocator.geocode(city)
        if not location:
            return jsonify({"error": "City not found"}), 404
        
        lat, lon = location.latitude, location.longitude

        # 2) Resolve coordinates to NWS Grid Points
        points_url = f"https://api.weather.gov/points/{lat},{lon}"
        points_res = requests.get(points_url, headers=HEADERS)
        points_res.raise_for_status()
        
        # 3) Get the Hourly Forecast URL
        forecast_url = points_res.json()['properties']['forecastHourly']
        forecast_res = requests.get(forecast_url, headers=HEADERS)
        forecast_res.raise_for_status()
        
        periods = forecast_res.json()['properties']['periods']
        
        # Current data is the first period
        current = periods[0]
        # Calculate H/L by looking at the next 24 hourly periods
        next_24h = periods[:24]
        temps = [p['temperature'] for p in next_24h]

        return jsonify({
            "city": city.split(',')[0].title(),
            "current_temp": current['temperature'],
            "high": max(temps),
            "low": min(temps),
            "condition": current['shortForecast'],
            "icon": current['icon'] # NWS provides direct icon URLs
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
