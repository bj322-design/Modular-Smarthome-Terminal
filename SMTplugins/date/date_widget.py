class DateWidget:
    def __init__(self):
        self.name = "Date"
        self.route = "/api/date"
        self.update_interval = 60

    def update(self):
        return {}