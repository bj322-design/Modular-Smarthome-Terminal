# sql.py
# Responsible for managing the internal SQL server that syncs smart devices across the home

import time

def thread():
    setup()
    while True:
        run()
        time.sleep(5)

def setup():
    print("Setting up sql...")

def run():
    print("SQL running...")