# calendarWidget.py
# Displays a monthly calendar with Google Calendar event integration (optional)
# Falls back to a static calendar view if no credentials are provided

from widget import Widget
from datetime import datetime, date
import calendar
import json

class calendarWidget(Widget):

    def __init__(self):
        self._preferences = self.widgetDefaultPreferences
        self._events = {}  # date_str -> list of event names

    @property
    def widgetName(self):
        return "Calendar Widget"

    @property
    def widgetID(self):
        return "easha:calendarwidget"

    @property
    def widgetHTML(self):
        """Returns the HTML template name; Flask renders it via Jinja."""
        return "calendar_widget.html"

    @property
    def widgetData(self):
        """Returns current calendar data as a JSON-serialisable dict."""
        today = date.today()
        year = today.year
        month = today.month

        cal = calendar.Calendar(firstweekday=6)  # week starts Sunday
        weeks = cal.monthdatescalendar(year, month)

        weeks_data = []
        for week in weeks:
            days = []
            for d in week:
                days.append({
                    "day": d.day,
                    "in_month": d.month == month,
                    "is_today": d == today,
                    "date_str": d.isoformat(),
                    "events": self._events.get(d.isoformat(), [])
                })
            weeks_data.append(days)

        return {
            "month_name": today.strftime("%B"),
            "year": year,
            "weeks": weeks_data,
            "day_headers": ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        }

    @property
    def widgetPreferences(self):
        return self._preferences

    @widgetPreferences.setter
    def widgetPreferences(self, value):
        self._preferences = value

    @property
    def widgetDefaultPreferences(self):
        return {
            "show_week_numbers": False,
            "use_google_cal": False,   # Set True + provide creds to enable
            "google_cal_id": "primary"
        }

    @property
    def updateTimer(self):
        # Refresh every 10 minutes
        return 600_000

    def update(self):
        """Called by the widget subsystem on a timer. Fetches events if enabled."""
        if self._preferences.get("use_google_cal"):
            self._fetch_google_events()
        else:
            # Placeholder: inject a couple of demo events so the UI isn't empty
            today = date.today().isoformat()
            self._events = {
                today: ["Class 4PM – LC 22", "Gym 5PM"]
            }
        print(f"Calendar Widget updated – {date.today().strftime('%B %Y')}")

    def _fetch_google_events(self):
        """
        Stub for Google Calendar API integration.
        To enable: install google-auth + google-api-python-client,
        create OAuth credentials, and fill in the logic below.
        """
        try:
            # TODO: implement OAuth flow and fetch events for current month
            # from googleapiclient.discovery import build
            # service = build("calendar", "v3", credentials=creds)
            # events_result = service.events().list(...).execute()
            raise NotImplementedError("Google Calendar auth not yet configured.")
        except Exception as e:
            print(f"[calendarWidget] Google Calendar fetch failed: {e}")

    def handle_event(self, event, args):
        """
        Supported events:
          - "prev_month"  : (future) navigate to previous month
          - "next_month"  : (future) navigate to next month
          - "add_event"   : args = {"date": "YYYY-MM-DD", "title": "..."}
        """
        if event == "add_event":
            date_str = args.get("date")
            title = args.get("title", "Event")
            if date_str:
                if date_str not in self._events:
                    self._events[date_str] = []
                self._events[date_str].append(title)
                print(f"[calendarWidget] Added event '{title}' on {date_str}")
        else:
            print(f"[calendarWidget] Unhandled event: {event} args={args}")