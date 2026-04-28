from widget import Widget


class FakeLightWidget(Widget):
    def __init__(self):
        self.id = "fake-light"
        self.state = "OFF"

    def widgetName(self):
        return "Fake Light"
    
    def widgetID(self):
        return self.id
    
    def widgetHTML(self):
        return "<div id='fake-light'></div>"
    
    def widgetData(self):
        return self.state
    
    def widgetPreferences(self):
        return {}
    
    def widgetDefaultPreferences(self):
        return {}

    def updateTimer(self):
        return 1000  # Refresh every 1 second to stay synced

    def update(self):
        return self.state

    def toggle(self):
        self.state = "ON" if self.state == "OFF" else "OFF"
        return self.state
    
    def handle_event(self, event, args):
        return None