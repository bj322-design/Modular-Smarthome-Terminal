# plugins.py
# Responsible for managing plugins and performing their runtime operations

import time

def thread():
    setup()
    run()

def setup():
    print("Setting up plugins...")

def run():
    print("Plugins running...")
    time.sleep(5)