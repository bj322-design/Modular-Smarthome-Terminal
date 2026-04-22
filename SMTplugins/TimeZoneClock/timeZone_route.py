from flask import Blueprint, jsonify
import json
import os
from datetime import datetime
import pytz

timeZone_bp = Blueprint('timeZone_bp', __name__)
DATA_FILE = os.path.join("SMTplugins", "TimeZoneClock", "locations.json")

@timeZone_bp.route("/api/timezone/data")
def get_location_times():
    output = []
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                # Iterate through L1, L2, L3
                for key in ["L1", "L2", "L3"]:
                    loc = data.get(key)
                    if loc:
                        tz = pytz.timezone(loc['tz'])
                        now = datetime.now(tz)
                        output.append({
                            "city": loc['city'],
                            "time": now.strftime("%I:%M %p"),
                            "label": loc['tz'].split('/')[-1].replace('_', ' ')
                        })
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    return jsonify(output)