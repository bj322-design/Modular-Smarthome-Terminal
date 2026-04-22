from widget import Widget
from datetime import datetime
import pytz
import json
import os

class timeZoneWidget(Widget):
    # Placeholders for the data
    times = ["--:--", "--:--", "--:--"]

    def widgetName(self):
        return "Time Zone"
    
    def widgetID(self):
        # This ID must match the one your JS uses: document.getElementById("time-zone")
        return "time-zone"
    
    def widgetHTML(self):
        # Your dynamic JS will inject content into this div
        return "<div id='time-zone'></div>"
    
    def widgetData(self):
        # Returns the current list of formatted times
        return self.times
    
    def widgetPreferences(self):
        return {}
    
    def widgetDefaultPreferences(self):
        return {}

    def updateTimer(self):
        return 10000  # Updates every 10 second to ensure clock accuracy
    
    def handle_event(self, event, args):
        return None

    def update(self, newtimes):
        self.times = newtimes
