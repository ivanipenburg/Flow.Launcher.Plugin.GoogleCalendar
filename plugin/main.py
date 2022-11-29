import copy
import os
import sys
from datetime import datetime

from ctparse import ctparse
from flowlauncher import FlowLauncher
from templates import *

parent_folder_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(parent_folder_path)
sys.path.append(os.path.join(parent_folder_path, "lib"))
sys.path.append(os.path.join(parent_folder_path, "lib", "plugin"))


class GoogleCalendar(FlowLauncher):
    def show_result(self, title, subtitle):
        return [
            {
                "Title": title,
                "SubTitle": subtitle,
                "IcoPath": "Images/app.png",
            }
        ]

    def query(self, query):
        if query == "":
            return self.show_result("No event name specified yet", "Please provide a name for your event")

        try:
            ts = datetime.now()
            parse = ctparse(query, ts=ts)
            if parse is None:
                return self.show_result("No date and time specified yet", "Please specify a date")

            start_dt = parse.resolution.start.dt
            end_dt = parse.resolution.end.dt

            event_name = query[:parse.resolution.mstart - 1]

            return self.show_result(f"Creating event '{event_name}'", f"from {start_dt} to {end_dt}")
            
        except:
            return self.show_result("Error", "Something went wrong")


if __name__ == "__main__":
    GoogleCalendar()
