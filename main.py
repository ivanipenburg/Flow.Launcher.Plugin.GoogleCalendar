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
    messages_queue = []

    def sendNormalMessage(self, title, subtitle):
        message = copy.deepcopy(RESULT_TEMPLATE)
        message["Title"] = title
        message["SubTitle"] = subtitle

        self.messages_queue.append(message)

    def query(self, query):
        print(query)
        try:
            ts = datetime.now()
            parse = ctparse(query, ts=ts)
            start_dt = parse.resolution.start.dt
            end_dt = parse.resolution.end.dt

            event_name = query[:parse.resolution.mstart - 1]

            self.sendNormalMessage(
                f"Creating event '{event_name}'", f"from {start_dt} to {end_dt}")
        except:
            self.sendNormalMessage("Error", "Something went wrong")

        return self.messages_queue


if __name__ == "__main__":
    GoogleCalendar()
