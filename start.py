# start.py
# Responsible for starting the thread manager and performing basic setup actions, such as
# checking for and initializing the settings file
# Also serves as the entry point for the program

from threading import Thread
import time
import sql
import flaskServer
import plugins
import atexit

# Starting script
def start():
    # Perform setup operations
    setup()

    # Initialize the threads
    sqlThread = Thread(target=sql.thread)
    sqlThread.daemon = True
    pluginsThread = Thread(target=plugins.thread)
    pluginsThread.daemon = True

    # Start the threads
    sqlThread.start()
    pluginsThread.start()
    flaskServer.run_flask()
    # Flask thread has to be run on the main thread because of signal
    #flaskServer.thread()

    # NOTE - Im gonna be kicking the can further down the road with this one but as it stands the way python threading works is
    # really silly, so I'm gonna remove all the debug loops and figure out how to kill all processes cleanly on exit at a later date.

# Perform setup operations
def setup():
    load_preferences()

# Load the preferences file or, if the preferences file is outdated, update it
def load_preferences():
    print("Preferences loading...")

# Start the program
if __name__ == '__main__':
    start()