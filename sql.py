# sql.py
# Responsible for managing the internal SQL server that syncs smart devices across the home

import time
import sqlite3

def thread():
    setup()



def setup():
    print("SQL Lite 3 SETUP RUNNING...")
    conn = sqlite3.connect('smt_database.db')
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''CREATE TABLE IF NOT EXISTS clients (id TEXT PRIMARY KEY, name TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS widgets (id TEXT PRIMARY KEY, name TEXT, class TEXT, css_name TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS client_layouts (
                        client_id TEXT, 
                        widget_id TEXT, 
                        row INTEGER, 
                        col INTEGER,
                        FOREIGN KEY(client_id) REFERENCES clients(id),
                        FOREIGN KEY(widget_id) REFERENCES widgets(id))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS widgetPrefs (
                        client_id TEXT,
                        widget_id TEXT,
                        prefs TEXT, 
                        FOREIGN KEY(client_id) REFERENCES clients(id),
                        FOREIGN KEY(widget_id) REFERENCES widgets(id))''')
    
    conn.commit()
    conn.close()
    print("...SQL Lite 3 SETUP COMPLETE")


def get_widget_preferences(client_id, widget_id):
    try:
        conn = sqlite3.connect('smt_database.db')
        cursor = conn.cursor()
        
        query = """SELECT widgetPrefs WHERE client_id = ? AND widget_id = ?"""
        pref = cursor.execute(query, (client_id, widget_id))
        if(pref):
            return pref
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()
        return None
    
    
    
def update_widget_preference(client_id, widget_id, new_prefs):
    try:
        conn = sqlite3.connect('smt_database.db')
        cursor = conn.cursor()
        
        # The UPDATE query
        query = """
            UPDATE widgetPrefs 
            SET prefs = ? 
            WHERE client_id = ? AND widget_id = ?
        """
        
        # Execute with parameters for security
        cursor.execute(query, (new_prefs, client_id, widget_id))
        
        # CRITICAL: Changes are not saved unless you commit
        conn.commit()
        
        if cursor.rowcount == 0:
            print("No rows were updated. Check if the ID exists.")
        else:
            print(f"Successfully updated {widget_id} for {client_id}")
            
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()



def addWidgetPref(widgetID, clientID, preferences):
    conn = sqlite3.connect('smt_database.db')
    cursor = conn.cursor()
    query = "INSERT INTO widgetPrefs (client_id, widget_id, prefs) VALUES (?, ?, ?)"
    data = (widgetID, clientID, preferences)
    cursor.execute(query, data)
    conn.commit()
    conn.close()


def add_client(clientName, clientID):
    conn = sqlite3.connect('smt_database.db')
    cursor = conn.cursor()
    query = "INSERT INTO clients (id, name) VALUES (?, ?)"
    data = (clientID, clientName)
    cursor.execute(query, data)
    conn.commit()
    conn.close()