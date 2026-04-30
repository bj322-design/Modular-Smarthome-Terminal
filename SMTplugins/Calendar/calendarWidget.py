# SMTplugins/Calendar/calendarWidget.py

from widget import Widget
from datetime import datetime, date, timedelta
import calendar
import json
import os
import time

# Google API Imports
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Calendar Read-Only Scope
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

class calendarWidget(Widget):

    def __init__(self):
        self._preferences = self.widgetDefaultPreferences
        self.file = "calendar_events.json"
        self._events = {}
        self.load_local_events()

    def load_local_events(self):
        if os.path.exists(self.file):
            with open(self.file, "r") as f:
                self._events = json.load(f)

    @property
    def widgetName(self):
        return "Calendar Widget"

    @property
    def widgetID(self):
        return "easha:calendarwidget"

    @property
    def widgetHTML(self):
        return "calendar_widget.html"

    @property
    def widgetData(self):
        today = date.today()
        year = today.year
        month = today.month

        cal = calendar.Calendar(firstweekday=6)
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
        return {}
    

    @property
    def widgetDefaultPreferences(self):
        return {
            "show_week_numbers": False,
            "use_google_cal": True, # Enabled by default for sync
            "google_cal_id": "primary"
        }

    def get_service(self):
        """Authenticated Google Calendar service helper."""
        creds = None
        # Paths consistent with SMT structure
        token_path = os.path.join("SMTplugins", "Calendar", "token_cal.json")
        creds_path = os.path.join("SMTplugins", "Calendar", "credentials.json")

        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
                creds = flow.run_local_server(port=0)
            with open(token_path, 'w') as token:
                token.write(creds.to_json())

        return build('calendar', 'v3', credentials=creds)

    def update(self):
        """Called by the subsystem to refresh data."""
        if self._preferences.get("use_google_cal"):
            self._fetch_google_events()
        else:
            if not self._events:
                # Default demo data
                today = date.today().isoformat()
                self._events[today] = [{"id": "demo1", "title": "Class 4PM – LC 22"}]

    def _fetch_google_events(self):
        """Fetches events for the current month and syncs to self._events."""
        try:
            service = self.get_service()
            now = datetime.utcnow()
            # Range: Start of current month to end of month
            start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0).isoformat() + 'Z'
            
            events_result = service.events().list(
                calendarId=self._preferences.get("google_cal_id", "primary"),
                timeMin=start_date,
                maxResults=100,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            google_events = events_result.get('items', [])
            
            # Temporary dict to avoid mixing old local events with fresh Google data
            new_events_map = {}

            for event in google_events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                # Extract just the YYYY-MM-DD part
                date_key = start[:10]
                
                if date_key not in new_events_map:
                    new_events_map[date_key] = []
                
                new_events_map[date_key].append({
                    "id": event['id'],
                    "title": event.get('summary', '(No Title)'),
                    "google_event": True
                })

            self._events = new_events_map
            # Persist to disk
            with open(self.file, "w") as f:
                json.dump(self._events, f)
                
        except Exception as e:
            print(f"[calendarWidget] Google Calendar sync failed: {e}")

    def updateTimer(self):
        return 60000  # Refresh every 1 minute to stay within API limits

    def handle_event(self, event, args):

    # -------- ADD TASK --------
        if event == "add_event":
            date_str = args.get("date")
            title = args.get("title", "Event")

            if date_str:
                if date_str not in self._events:
                    self._events[date_str] = []

                self._events[date_str].append({
                    "id": int(time.time()*1000),
                    "title": title
                })

                self._save_events()

        # -------- NEXT MONTH --------
        elif event == "next_month":
            print("NEXT MONTH TRIGGERED")

            if self.current_date.month == 12:
                self.current_date = self.current_date.replace(
                    year=self.current_date.year + 1,
                    month=1
                )
            else:
                self.current_date = self.current_date.replace(
                    month=self.current_date.month + 1
                )

            self._save_state()
            print("NEW MONTH:", self.current_date)

        # -------- PREVIOUS MONTH --------
        elif event == "prev_month":
            print("PREV MONTH TRIGGERED")

            if self.current_date.month == 1:
                self.current_date = self.current_date.replace(
                    year=self.current_date.year - 1,
                    month=12
                )
            else:
                self.current_date = self.current_date.replace(
                    month=self.current_date.month - 1
                )

            self._save_state()
            print("NEW MONTH:", self.current_date)

        else:
            print(f"[calendarWidget] Unhandled event: {event} args={args}")