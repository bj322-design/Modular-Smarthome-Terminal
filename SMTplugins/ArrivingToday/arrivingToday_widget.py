import os
import json
import base64
from datetime import datetime
from widget import Widget
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

class ArrivingTodayWidget(Widget):
    def widgetName(self):
        return "Arriving Today"

    def widgetID(self):
        return "arriving_today"

    def widgetHTML(self):
        return "<div id='arriving_today_container' class='package-widget'>Loading Gmail updates...</div>"

    def get_service(self):
        creds = None
        # Look for token in the plugin directory
        token_path = os.path.join(os.path.dirname(__file__), 'token.json')
        creds_path = os.path.join(os.path.dirname(__file__), 'credentials.json')

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

        return build('gmail', 'v1', credentials=creds)

    def widgetData(self, client_id=None):
        try:
            service = self.get_service()
            # Search for emails from the last 48 hours containing delivery keywords
            # We look for "out for delivery" or "delivered today"
            query = 'newer_than:2d ("out for delivery" OR "arriving today" OR "delivering today")'
            results = service.users().messages().list(userId='me', q=query).execute()
            messages = results.get('messages', [])

            arriving_packages = []
            
            for msg in messages:
                m = service.users().messages().get(userId='me', id=msg['id']).execute()
                headers = m['payload']['headers']
                subject = next(h['value'] for h in headers if h['name'] == 'Subject')
                sender = next(h['value'] for h in headers if h['name'] == 'From')
                
                # Simple logic to extract a "Carrier" name from common senders
                carrier = "Package"
                if "amazon" in sender.lower(): carrier = "Amazon"
                elif "ups" in sender.lower(): carrier = "UPS"
                elif "fedex" in sender.lower(): carrier = "FedEx"
                elif "usps" in sender.lower(): carrier = "USPS"

                arriving_packages.append({
                    "name": subject,
                    "carrier": carrier,
                    "status": "Out for Delivery"
                })

            return {
                "count": len(arriving_packages),
                "packages": arriving_packages,
                "last_updated": datetime.now().strftime("%H:%M")
            }

        except Exception as e:
            print(f"Gmail Widget Error: {e}")
            return {"count": 0, "packages": [], "error": str(e)}
    
    def handle_event(self, event, args):
        return super().handle_event(event, args)
    
    @property
    def updateTimer(self):
        return 60000
    
    @property
    def widgetDefaultPreferences(self):
        return super().widgetDefaultPreferences
    

    @property
    def widgetPreferences(self):
        return super().widgetPreferences
    
    def update(self):
        return super().update()