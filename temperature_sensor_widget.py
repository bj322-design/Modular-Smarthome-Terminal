from widget import Widget

class tempSensorWidget(Widget):
    temperature = 0
    C_or_F = "F"

    def widgetName(self):
        return "Temp Sensor"
    
    def widgetID(self):
        return "temperature"
    
    def widgetHTML(self):
        return "<div id='temperature'></div>"
    
    def widgetData(self):
        return self.temperature + self.C_or_F
    
    def widgetPreferences(self):
        return {}
    
    def widgetDefaultPreferences(self):
        return {}
    
    def updateTimer(self):
        return 2000 #updates every 2 seconds
    
    def handle_event(self, event, args):
        return None
    
    def update(self):
        return self.temperature + self.C_or_F
    

    def updateTemp(self, temp):
        self.temperature = temp