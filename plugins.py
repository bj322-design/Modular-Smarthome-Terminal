# plugins.py
# Responsible for managing plugins and performing their runtime operations

import time
import widget
from debugWidget import debugWidget

def thread():
    setup()
    while True:
        run()
        time.sleep(5)

def setup():
    widgetSubsystem.instance = widgetSubsystem()
    widgetSubsystem.instance.addWidget(debugWidget())

def run():
    print("Widgets Subsystem Running")
    widgetSubsystem.instance.update()

# widgetSubsystem
# Class that manages the operation, addition, removal, and sending commands to widgets
class widgetSubsystem:
    # Instance is a static variable used to obtain the current-running widget subsystem
    instance = None

    def __init__(self):
        if widgetSubsystem.instance is not None:
            raise RuntimeError("Another widget subsystem was initialized while one was already running")

        # Variables for internal use
        # Widget List - Dictionary of widgets indexed by widget ID
        self.widgetList = dict()
        # Widget Outputs - Dictionary of widget outputs indexed by widget ID. Allows widget to define their own output structure
        self.widgetOutputs = dict()
        # Last Updated - Non persistent dictionary saying when each widget had last been updated
        self.lastUpdated = dict()

    # Returns a list of widgets available for installation. Requires external server connection
    def getAvailableWidgets():
        raise NotImplementedError()

    # Returns the dictionary of all installed widgets
    def getInstalledWidgets(self):
        return self.widgetList

    # Function for adding a widget to the current list
    def addWidget(self, widget):
        self.widgetList.update({widget.widgetID: widget})
        return

    # Removes the widget with the associated widgetID from the widget list
    def removeWidget(self, widgetID):
        self.widgetList.pop(widgetID)
        return

    # Retrieves the preferences from the widget with the given ID
    def getWidgetPreferences(self, widgetID):
        return self.widgetList[widgetID].widgetPreferences

    # Sets the preferences for the widget with the given ID
    def setWidgetPreferences(self, widgetID, preferences):
        self.widgetList[widgetID].widgetPreferences = preferences
        return

    # Sends the given command to the given widget
    def sendCommandToWidget(self, widgetID, command, args):
        self.widgetList[widgetID].handle_event(command, args)

    # Handles the updating of each widget
    def update(self):
        # For each widget in the list
        for key in self.widgetList.keys():
            # Get the current time
            currentTime = int(time.time() * 1000)

            # Get the current widget
            widget = self.widgetList[key]

            # If there is no matching key in the update list (Has never updated), or the difference between the current and last time is greater than the update timer, update the widget
            if (key not in self.lastUpdated.keys()) or ((currentTime - self.lastUpdated[key]) >= widget.updateTimer):
                widget.update()
                # Update the widget's last updated timer to the current time
                self.lastUpdated.update({key: currentTime})

