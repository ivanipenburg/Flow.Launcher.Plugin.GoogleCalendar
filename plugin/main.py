import webbrowser
from datetime import datetime

from apiclient import discovery
from credentials import credentials_exist, get_credentials
from ctparse import ctparse
from events import get_event_times, get_sorted_events
from flox import Flox
from icons import date_to_glyph_id
from templates import EVENT

SETUP_URL = "https://github.com/ivanipenburg/Flow.Launcher.Plugin.GoogleCalendar#setup"
TIME_FORMAT = "%Y-%m-%dT%H:%M:%S"
NUM_UPCOMING_EVENTS = 20


class GoogleCalendar(Flox):
    def __init__(self):
        super().__init__()
        self.font_family = "#Date-Icons"
        self.upcoming_events = []


    def show_result(self, title, subtitle, score=99, glyph_id="", method=None, params=None):
        self.add_item(
            title=title,
            subtitle=subtitle,
            score=score,
            glyph=glyph_id,
            method=method,
            parameters=params,
        )
    

    def query(self, query):
        if not credentials_exist():
            return self.show_result("It seems like you have not set up your credentials yet", "Press Enter to open the setup page", method="open_webpage", params=[SETUP_URL])

        if query == "":
            self.show_result("No event name specified yet", "Please provide a name for your event")

        self.display_current_events()

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

            return self.show_result(f"Creating event '{event_name}'", f"from {start_dt} to {end_dt}", method="create_event", params=[event_name, start_dt_string, end_dt_string])
        except Exception as e:
            return self.show_result("Error", str(e))


    def open_webpage(self, url):
        webbrowser.open(url)


    def create_event(self, event_name, start_dt, end_dt):
        credentials = get_credentials()

        try:
            service = discovery.build('calendar', 'v3', credentials=credentials)

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


    def display_current_events(self):
        credentials = get_credentials()

        self.show_result("Upcoming events", "", score=40)
        
        if self.upcoming_events == []:
            try:
                service = discovery.build('calendar', 'v3', credentials=credentials)

                all_events = get_sorted_events(service, NUM_UPCOMING_EVENTS)
                self.upcoming_events = all_events
            except Exception as e:
                self.show_result('Could not load upcoming events', e)

        for i, event in enumerate(self.upcoming_events):
            if 'summary' not in event:
                continue

            start_dt, _, start_time, end_time = get_event_times(event, TIME_FORMAT)

            location = event['location'] if 'location' in event else None

            subtitle = ""
            if start_time is not None and end_time is not None:
                subtitle += f"{start_time} - {end_time}"
            if location is not None:
                subtitle += f" @ {location}"

            date_glyph_id = date_to_glyph_id(start_dt)                
            self.show_result(event['summary'], subtitle, score=10-i, glyph_id=date_glyph_id, method="open_webpage", params=[event['htmlLink']])
        

if __name__ == "__main__":
    GoogleCalendar()
