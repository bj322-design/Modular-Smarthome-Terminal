# debugWidget.py
# Example implementation of an extremely simple widget. Used for testing

from widget import Widget

class debugWidget(Widget):
    @property
    def widgetName(self):
        return "Debug Widget"

    @property
    def widgetID(self):
        return "beadugan:debugwidget"

    @property
    def widgetHTML(self):
        return None

    @property
    def widgetData(self):
        return None

    @property
    def widgetPreferences(self):
        return None

    @property
    def widgetDefaultPreferences(self):
        return None

    @property
    def updateTimer(self):
        return 5000

    def update(self):
        print("Debug Widget Running!")

    def handle_event(self, event, args):
        print("Debug Widget Sent Command " + str(event) + " with arguments " + str(args))
