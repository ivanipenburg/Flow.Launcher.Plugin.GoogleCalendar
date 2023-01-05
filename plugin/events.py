from datetime import datetime


def get_sorted_events(service, num_events):
    calendars = service.calendarList().list().execute()

    all_events = []

    # Get all events of the user
    for calendar in calendars['items']:
        events =  service.events().list(calendarId=calendar['id'], timeMin=datetime.utcnow().isoformat() + 'Z', maxResults=num_events, singleEvents=True, orderBy='startTime').execute()

        all_events += events['items']

        # Sort all events by start date
        all_events = sorted(all_events, key=lambda k: k['start']['dateTime'] if 'dateTime' in k['start'] else k['start']['date'])

    return all_events[:num_events]


def get_event_times(event, time_format):
    
    start_dt, end_dt, start_time, end_time = None, None, None, None
    if 'dateTime' in event['start']:
        start_dt = datetime.strptime(event['start']['dateTime'][:19], time_format)
        end_dt = datetime.strptime(event['end']['dateTime'][:19], time_format)

        start_time = start_dt.strftime("%H:%M")
        end_time = end_dt.strftime("%H:%M")
    else:
        start_dt = datetime.strptime(event['start']['date'], "%Y-%m-%d")

    return start_dt, end_dt, start_time, end_time