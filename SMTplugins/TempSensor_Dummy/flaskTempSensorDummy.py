from SMTplugins.TempSensor_Dummy.temperature_sensor_widget import tempSensorWidget
from flask import jsonify, Blueprint
import os
import json

fTemp_bp = Blueprint('FakeTeperature', __name__)

DATA_FILE = "SMTplugins/TempSensor_Dummy/sensor_data.json"

@fTemp_bp.route("/temperature")
def get_temp():
    current_val = "NAN "
    
    # Check if the file exists before trying to read it
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                current_val = str(data.get("temperature"))
        except Exception as e:
            print(f"Error reading JSON file: {e}")

    # Pass the value to Widget Subsystem
    temp_widget = tempSensorWidget()
    temp_widget.updateTemp(current_val) 
    return jsonify({"temp": temp_widget.update()})

    #FOR HOME ASSISTANT UNTESTED
    # try:
    #     # Synchronously pull the latest RETAINED message from the broker
    #     # timeout=1 ensures the webpage doesn't hang if the broker is down
    #     msg = subscribe.simple("home/pi/sensor", hostname="127.0.0.1", timeout=1)
    #     payload = json.loads(msg.payload.decode())
    #     val = str(payload.get("temperature", "0"))
    # except Exception:
    #     val = "0" # Fallback if broker is unreachable
###################################################
