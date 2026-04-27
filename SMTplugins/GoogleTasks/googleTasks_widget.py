from widget import Widget
import os.path
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/tasks']

class GoogleTasksWidget(Widget):

    def widgetName(self):
        return "Google Tasks"
    
    def widgetID(self):
        return "google-tasks"
    
    def widgetHTML(self):
        return "<div id='google-tasks'>Loading tasks...</div>"

    def widgetData(self):
        return self.temperature + self.C_or_F
    
    def widgetPreferences(self):
        return {}
    
    def widgetDefaultPreferences(self):
        return {}

    def updateTimer(self):
        return 60000  # Refresh every 1 minute to stay within API limits

    def handle_event(self, event, args):
        return None

    def get_service(self):
        """Helper to get the authenticated Google Tasks service."""
        creds = None
        # Use absolute or relative paths consistent with your SMT structure
        token_path = os.path.join("SMTplugins", "GoogleTasks", "token.json")
        creds_path = os.path.join("SMTplugins", "GoogleTasks", "credentials.json")

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

        return build('tasks', 'v1', credentials=creds)

    def update(self):
        """Fetches list name and tasks to match JS expectation."""
        try:
            service = self.get_service()
            
            # Fetch List Name (Default list)
            list_info = service.tasklists().get(tasklist='@default').execute()
            list_name = list_info.get('title', 'My Tasks')

            # Fetch Tasks (Not completed)
            results = service.tasks().list(tasklist='@default', showCompleted=False).execute()
            items = results.get('items', [])
            
            # Formatting to match: data.tasks and data.list_name
            return {
                "list_name": list_name,
                "tasks": [{"id": t['id'], "title": t['title']} for t in items]
            }
        except Exception as e:
            print(f"Google Tasks update error: {e}")
            return {"list_name": "Sync Error", "tasks": []}