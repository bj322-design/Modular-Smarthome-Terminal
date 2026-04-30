from flask import Flask, render_template, request, jsonify
import os
import json

'''from SMTplugins.pluginImports import *
from SMTplugins.Calendar.calendar_plugin import calendar_bp
from SMTplugins.Package.package_plugin import package_bp
'''

app = Flask(__name__)



#######PLUGINS#######
'''app.register_blueprint(clock_bp)
app.register_blueprint(fTemp_bp)
app.register_blueprint(weather_bp)
app.register_blueprint(timeZone_bp)
app.register_blueprint(date_bp)
app.register_blueprint(blackjack_bp) #Blackjack
app.register_blueprint(googleTasks_bp)
app.register_blueprint(spotify_bp)
app.register_blueprint(calendar_bp)
app.register_blueprint(package_bp)
app.register_blueprint(fakeLight_bp)
'''


#allows for easier starting of flask from start file
def run_flask():
    app.run(debug=True, port=5000, use_reloader=False)



@app.route("/")
def clientHome():
    # This could be from a database for now its json layout_client.json
    DATA_FILE = "layout_client.json"
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    
    # Passes the list of widgets to the template
    return render_template('index.html', widgets=data['widgets'])
    #return render_template("index.html")
  
@app.route("/settings")
def settings():
    return render_template("settingspage.html")

# Slated for removal-- starting through start.py now
if __name__ == '__main__':
    app.run(debug=True)



@app.route("/api/layout", methods=["GET"])
def get_layout():
    with open("layout_client.json", "r") as file:
        layout = json.load(file)
    return jsonify(layout)


@app.route("/api/layout", methods=["POST"])
def save_layout():
    new_layout = request.json

    with open("layout_client.json", "w") as file:
        json.dump(new_layout, file, indent=4)

    return jsonify({"message": "Layout saved"})


@app.route("/api/layout/default", methods=["POST"])
def reset_layout():
    with open("default_layout_client.json", "r") as file:
        default_layout = json.load(file)

    with open("layout_client.json", "w") as file:
        json.dump(default_layout, file, indent=4)

    return jsonify(default_layout)


if __name__ == '__main__':
    app.run(debug=True)