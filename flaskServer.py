from flask import Flask, render_template
from flask import jsonify, request
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
app.register_blueprint(arriving_today_bp)



#allows for easier starting of flask from start file
def run_flask():
    app.run(host='0.0.0.0', debug=True, port=5000, use_reloader=False)



@app.route("/")
def clientHomeStart():
    return render_template('start_page.html')
    '''# This could be from a database for now its json layout_client.json
    DATA_FILE = "layout_client.json"
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    
    # Passes the list of widgets to the template
    return render_template('index.html', widgets=data['widgets'])
    #return render_template("index.html");'''


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

    
  
@app.route('/settings')
def settings():
    conn = sqlite3.connect('smt_database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Fetch all registered clients for the dropdown
    cursor.execute("SELECT id, name FROM clients")
    clients = cursor.fetchall()

    # Fetch all available widgets to display in the box format
    cursor.execute("SELECT * FROM widgets")
    available_widgets = cursor.fetchall()
    
    conn.close()
    return render_template('settingspage.html', clients=clients, available_widgets=available_widgets)

@app.route('/api/get_layout/<client_id>')
def get_layout(client_id):
    conn = sqlite3.connect('smt_database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT widget_id, row, col FROM client_layouts WHERE client_id = ?", (client_id,))
    layout = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(layout)


# ── ADD THIS IMPORT at the top of flaskServer.py ──
# from flask import request

# ── ADD THIS ROUTE to flaskServer.py ──
@app.route('/api/save_layout', methods=['POST'])
def save_layout():
    data = request.get_json()
    client_id = data.get('client_id')
    layout    = data.get('layout', [])   # [{widget_id, row, col}, ...]

    if not client_id:
        return jsonify({'error': 'client_id required'}), 400

    conn = sqlite3.connect('smt_database.db')
    cursor = conn.cursor()

    # Replace the client's layout entirely
    cursor.execute("DELETE FROM client_layouts WHERE client_id = ?", (client_id,))
    for entry in layout:
        cursor.execute(
            "INSERT INTO client_layouts (client_id, widget_id, row, col) VALUES (?, ?, ?, ?)",
            (client_id, entry['widget_id'], entry['row'], entry['col'])
        )

    conn.commit()
    conn.close()

    return jsonify({'message': f"Layout saved for {client_id} ({len(layout)} widgets)"})

@app.route('/api/get_prefs/<client_id>')
def get_prefs(client_id):
    conn = sqlite3.connect('smt_database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Fetch preferences for this specific client
    cursor.execute("SELECT widget_id, prefs FROM widgetPrefs WHERE client_id = ?", (client_id,))
    prefs = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(prefs)

@app.route('/api/save_prefs', methods=['POST'])
def save_prefs():
    data = request.get_json()
    client_id = data.get('client_id')
    prefs_list = data.get('prefs', []) # Expects [{widget_id: "...", prefs: "..."}, ...]

    if not client_id:
        return jsonify({'error': 'client_id required'}), 400

    conn = sqlite3.connect('smt_database.db')
    cursor = conn.cursor()

    for item in prefs_list:
        w_id = item.get('widget_id')
        val = item.get('prefs')
        
        # Use an INSERT OR REPLACE (UPSERT) logic
        # First, check if a preference exists
        cursor.execute("SELECT 1 FROM widgetPrefs WHERE client_id = ? AND widget_id = ?", (client_id, w_id))
        if cursor.fetchone():
            cursor.execute(
                "UPDATE widgetPrefs SET prefs = ? WHERE client_id = ? AND widget_id = ?",
                (val, client_id, w_id)
            )
        else:
            cursor.execute(
                "INSERT INTO widgetPrefs (client_id, widget_id, prefs) VALUES (?, ?, ?)",
                (client_id, w_id, val)
            )

    conn.commit()
    conn.close()
    return jsonify({'message': 'Preferences updated successfully'})




@app.route('/api/create_client', methods=['POST'])
def create_client():
    data = request.get_json()
    client_id = data.get('client_id')
    
    if not client_id:
        return jsonify({'error': 'Client ID is required'}), 400

    try:
        conn = sqlite3.connect('smt_database.db')
        cursor = conn.cursor()

        # Check if client already exists to avoid duplicates
        cursor.execute("SELECT id FROM clients WHERE id = ?", (client_id,))
        if cursor.fetchone():
            conn.close()
            return jsonify({'message': 'Client already exists', 'client_id': client_id}), 200

        # Insert the new client into the clients table
        # Note: 'name' is set to the ID as a default if your table requires a name
        cursor.execute("INSERT INTO clients (id, name) VALUES (?, ?)", (client_id, client_id))
        
        conn.commit()
        conn.close()
        return jsonify({'message': 'Client created successfully', 'client_id': client_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route('/api/rename_client', methods=['POST'])
def rename_client():
    data = request.get_json()
    client_id = data.get('client_id')
    new_name = data.get('new_name')
    
    conn = sqlite3.connect('smt_database.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE clients SET name = ? WHERE id = ?", (new_name, client_id))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

@app.route('/api/delete_client', methods=['POST'])
def delete_client():
    data = request.get_json()
    client_id = data.get('client_id')
    
    conn = sqlite3.connect('smt_database.db')
    cursor = conn.cursor()
    # Remove client and their specific layout settings
    cursor.execute("DELETE FROM clients WHERE id = ?", (client_id,))
    cursor.execute("DELETE FROM client_layouts WHERE client_id = ?", (client_id,))
    cursor.execute("DELETE FROM widgetPrefs WHERE client_id = ?", (client_id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

# Slated for removal-- starting through start.py now
if __name__ == '__main__':
    app.run(debug=True)
