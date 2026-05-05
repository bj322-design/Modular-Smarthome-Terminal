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
    conn.commit()
    conn.close()
    print("...SQL Lite 3 SETUP COMPLETE")
