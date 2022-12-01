import copy
import json
import os
import sys
import webbrowser
from datetime import datetime

import httplib2
from apiclient import discovery
from ctparse import ctparse
from flowlauncher import FlowLauncher
from oauth2client import client, file, tools
from templates import *

SCOPES = 'https://www.googleapis.com/auth/calendar'
APPLICATION_NAME = 'Google Calendar Flow Launcher Plugin'
CLIENT_ID = None
PROJECT_ID = None
CLIENT_SECRET = None
CLIENT_SECRET_FILE = 'credentials/credentials.json'

def open_webpage(url):
    webbrowser.open(url)


def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    credential_path = os.path.join(credential_dir, 'calendar-python.json')
    
    store = file.Storage(credential_path)
    credentials = store.get()

    # if not credentials or credentials.invalid:
    #     if not os.path.exists(CLIENT_SECRET_FILE):
    #         # Create client secret file
    #         client_secret_file = {
    #             "installed": {
    #                 "client_id": CLIENT_ID,
    #                 "project_id": PROJECT_ID,
    #                 "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    #                 "token_uri": "https://accounts.google.com/o/oauth2/token",
    #                 "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    #                 "client_secret": CLIENT_SECRET,
    #                 "redirect_uris": ["http://localhost"]
    #             }
    #         }
            
    #         # Create JSON file from dictionary
    #         with open(CLIENT_SECRET_FILE, 'w') as outfile:
    #             json.dump(client_secret_file, outfile)

    #     flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
    #     flow.user_agent = APPLICATION_NAME
    #     credentials = tools.run_flow(flow, store)
    #     # print('Storing credentials to ' + credential_path)

    return credentials



class GoogleCalendar(FlowLauncher):
    def show_result(self, title, subtitle):
        return [
            {
                "Title": title,
                "SubTitle": subtitle,
                "IcoPath": "Images/app.png",
            }
        ]

    def action_result(self, title, subtitle, action, params):
        return [
            {
                "Title": title,
                "SubTitle": subtitle,
                "IcoPath": "Images/app.png",
                "JsonRPCAction": {
                    "method": action,
                    "parameters": params,
                }
            }
        ]

    def query(self, query):
        # Load settings
        # global CLIENT_ID, PROJECT_ID, CLIENT_SECRET
        # if not CLIENT_ID or not PROJECT_ID or not CLIENT_SECRET:
        #     settings = self.rpc_request.get("settings", {})
        #     if client_id := settings.get("client_id"):
        #         CLIENT_ID = client_id
        #     else:
        #         return self.action_result("It seems like you haven't set up your API information yet", "Press Enter to open the instructions page", "open_webpage", ["https://github.com/ivanipenburg/Flow.Launcher.Plugin.GoogleCalendar"])
        #     if project_id := settings.get("project_id"):
        #         PROJECT_ID = project_id
        #     else:
        #         return self.action_result("It seems like you haven't set up your Google Cloud API yet", "Press Enter to open the instructions page", "open_webpage", ["https://github.com/ivanipenburg/Flow.Launcher.Plugin.GoogleCalendar"])
        #     if client_secret := settings.get("client_secret"):
        #         CLIENT_SECRET = client_secret
        #     else:
        #         return self.action_result("It seems like you haven't set up your API information yet", "Press Enter to open the instructions page", "open_webpage", ["https://github.com/ivanipenburg/Flow.Launcher.Plugin.GoogleCalendar"])


        if query == "":
            return self.show_result("No event name specified yet", "Please provide a name for your event")

        try:
            ts = datetime.now()
            parse = ctparse(query, ts=ts)
            if parse is None:
                return self.show_result("No date and time specified yet", "Please specify a date")

            start_dt = parse.resolution.start.dt
            end_dt = parse.resolution.end.dt

            start_dt_string = start_dt.strftime("%Y-%m-%dT%H:%M:%S")
            end_dt_string = end_dt.strftime("%Y-%m-%dT%H:%M:%S")

            event_name = query[:parse.resolution.mstart - 1]

            return self.action_result(f"Creating event '{event_name}'", f"from {start_dt} to {end_dt}", "create_event", [event_name, start_dt_string, end_dt_string])
            
        except Exception as e:
            return self.show_result("Error", str(e))

    def create_event(self, event_name, start_dt, end_dt):
        credentials = get_credentials()
        try:
            http = credentials.authorize(httplib2.Http())
            service = discovery.build('calendar', 'v3', http=http)

            # Get the timezone of the user
            user_info = service.calendarList().get(calendarId='primary').execute()
            timezone = user_info['timeZone']
            
            event = {
                'summary': event_name,
                'start': {
                    'dateTime': start_dt,
                    'timeZone': timezone,
                },
                'end': {
                    'dateTime': end_dt,
                    'timeZone': timezone,
                },
            }

            event = service.events().insert(calendarId='primary', body=event).execute()
            self.show_result('Event created: %s' % (event.get('htmlLink')), "")
        except Exception as e:
            self.show_result('Error', e)


if __name__ == "__main__":
    GoogleCalendar()