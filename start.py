# start.py
# Responsible for starting the thread manager and performing basic setup actions, such as
# checking for and initializing the settings file
# Also serves as the entry point for the program

import threading
import time
import sql
import flaskServer
import plugins

# Starting script
def start():
    # Perform setup operations
    setup()

    # Initialize the threads
    sqlThread = threading.Thread(target=sql.thread(), daemon = True)
    pluginsThread = threading.Thread(target=plugins.thread(), daemon = True)
    flaskThread = threading.Thread(target=flaskServer.thread(), daemon = True)

    # Start the threads
    sqlThread.start()
    pluginsThread.start()
    flaskThread.start()

# Perform setup operations
def setup():
    load_preferences()

# Load the preferences file or, if the preferences file is outdated, update it
def load_preferences():
    print("Preferences loading...")

# Start the program
if __name__ == '__main__':
    start()