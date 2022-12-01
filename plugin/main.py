import copy
import os
import webbrowser
from datetime import datetime

import httplib2
from apiclient import discovery
from credentials import credentials_exist, get_credentials
from ctparse import ctparse
from flowlauncher import FlowLauncher
from templates import ACTION_RESULT, EVENT, SHOW_RESULT

SETUP_URL = "https://github.com/ivanipenburg/Flow.Launcher.Plugin.GoogleCalendar#setup"
TIME_FORMAT = "%Y-%m-%dT%H:%M:%S"


def open_webpage(url):
    webbrowser.open(url)


class GoogleCalendar(FlowLauncher):

    def show_result(self, title, subtitle):
        result = SHOW_RESULT.copy()
        result["Title"] = title
        result["SubTitle"] = subtitle
        return [result]


    def action_result(self, title, subtitle, action, params):
        result = ACTION_RESULT.copy()
        result["Title"] = title
        result["SubTitle"] = subtitle
        result["JsonRPCAction"]["method"] = action
        result["JsonRPCAction"]["parameters"] = params
        return [result]


    def query(self, query):
        if not credentials_exist():
            return self.action_result("It seems like you have not set up your credentials yet", "Press Enter to open the setup page", "open_webpage", [SETUP_URL])

        if query == "":
            return self.show_result("No event name specified yet", "Please provide a name for your event")

        try:
            ts = datetime.now()
            parse = ctparse(query, ts=ts)
            if parse is None:
                return self.show_result("No date and time specified yet", "Please specify a date")

            start_dt = parse.resolution.start.dt
            end_dt = parse.resolution.end.dt

            start_dt_string = start_dt.strftime(TIME_FORMAT)
            end_dt_string = end_dt.strftime(TIME_FORMAT)

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
            
            event = EVENT.copy()
            event["summary"] = event_name
            event["start"]["dateTime"] = start_dt
            event["start"]["timeZone"] = timezone
            event["end"]["dateTime"] = end_dt
            event["end"]["timeZone"] = timezone

            event = service.events().insert(calendarId='primary', body=event).execute()
            
        except Exception as e:
            self.show_result('Error', e)


if __name__ == "__main__":
    GoogleCalendar()