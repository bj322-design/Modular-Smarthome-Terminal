from flask import Blueprint, jsonify, request
import requests
from geopy.geocoders import Nominatim
import os
import json
import sqlite3
from sql import update_widget_preference, addWidgetPref

weather_bp = Blueprint('weather_bp', __name__)
geolocator = Nominatim(user_agent="SMT_Terminal_Project")

# NWS requires a unique User-Agent header
HEADERS = {
    'User-Agent': '(SMT-Project, bschadoff@albany.edu)',
    'Accept': 'application/geo+json'
}

DATA_FILE = "SMTplugins/Weather/weather_city.json"

def Default():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                currentVal = str(data.get("city"))
                return currentVal
        except Exception as e:
            print(f"Error reading JSON File: {e}")
            



@weather_bp.route('/api/weather/smt', methods=['GET'])
def get_nws_weatherClient():
    clientID = request.args.get('client_id', 'default_id')
    conn = sqlite3.connect('smt_database.db')
    cursor = conn.cursor()
    currentVal = None
    if(clientID == None):
        print("DEFAULT**************************")
        currentVal = Default()
    else:
        try:
            print(f"CLIENT ID py", clientID)
            cursor.execute("SELECT prefs FROM widgetPrefs WHERE client_id = ? AND widget_id = ?", (clientID, "weather"))
            result = cursor.fetchone()
            currentVal = result[0]
            print(f'*******************{currentVal}, {clientID}')
            conn.close()
        except Exception as e:
            print("error", 501)


    if(currentVal == None):
        print("DEFAULT**************************")
        currentVal = Default()

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

@weather_bp.route('/api/weather/smt/changeCity/<city><clientID>', methods=['GET'])
def changeCity(city, clientID):
    sql.update_widget_preferences('weather', clientID, city)


'''@weather_bp.route('/api/weather/smt', methods=['GET'])
def get_nws_weather():

    currentVal = Default()

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
    
    '''