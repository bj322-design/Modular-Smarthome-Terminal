from flask import Flask, render_template
from flask import Flask
from flask import jsonify
import os
import json
import sqlite3

from SMTplugins.pluginImports import *
from SMTplugins.Calendar.calendar_plugin import calendar_bp
from SMTplugins.Package.package_plugin import package_bp

app = Flask(__name__)



#######PLUGINS#######
app.register_blueprint(clock_bp)
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



#allows for easier starting of flask from start file
def run_flask():
    app.run(debug=True, port=5000, use_reloader=False)



@app.route("/")
def clientHomeStart():
    # This could be from a database for now its json layout_client.json
    DATA_FILE = "layout_client.json"
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    
    # Passes the list of widgets to the template
    return render_template('index.html', widgets=data['widgets'])
    #return render_template("index.html")


@app.route("/<client_id>")
def clientHome(client_id):
    conn = sqlite3.connect('smt_database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Query the database for this specific client's widgets
    query = '''
        SELECT w.id, w.name, w.class, w.css_name, cl.row, cl.col 
        FROM widgets w
        JOIN client_layouts cl ON w.id = cl.widget_id
        WHERE cl.client_id = ?
    '''
    cursor.execute(query, (client_id,))
    widgets = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return render_template('index.html', widgets=widgets, client_id=client_id)

    
  
@app.route("/settings")
def settings():
    return render_template("settingspage.html")

# Slated for removal-- starting through start.py now
if __name__ == '__main__':
    app.run(debug=True)
