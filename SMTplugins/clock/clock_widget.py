from widget import Widget
from datetime import datetime

class clockWidget(Widget):

    def widgetName(self):
        return "Clock"

    def widgetID(self):
        return "clock"

    def widgetHTML(self):
        return "<div id='clock'></div>"

    def widgetData(self):
        return datetime.now().strftime("%I:%M:%S %p")
        

    def widgetPreferences(self):
        return {}

    def widgetDefaultPreferences(self):
        return {}

    def updateTimer(self):
        return 1000  # update every 1 second

    def handle_event(self, event, args):
        return None

    def update(self):
        return datetime.now().strftime("%I:%M:%S %p")