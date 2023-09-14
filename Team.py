import requests
from ApiCalls import TBA

class TeamData():
    events = []

    def __init__(self, team):
        self.tba = TBA()

        event_data = self.tba.get_data("/team/frc" + team + "/events")
        for event in event_data:
            week = event["week"]
            if(week is not None) and int(event["year"]) >= 2020:
                key = event["key"]
                lat = event["lat"]
                lng = event["lng"]
                self.events.append([key, week, [lat, lng]])
        print(self.events)


T4909 = TeamData("4909")

