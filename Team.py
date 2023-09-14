import requests
from ApiCalls import TBA

class TeamData():
    events = []

    def __init__(self, team):
        self.tba = TBA()
        self.team = team
        self.events = self.get_events()
        print(self.events)

        

    def get_events(self):
        event_data = self.tba.get_data("/team/frc" + self.team + "/events")
        events = []
        for event in event_data:
            week = event["week"]
            year = int(event["year"])
            if(event["event_type"] <= 5 and year >= 2020 and year != 2021):
                lat = float(event["lat"])
                lng = float(event["lng"])
                if(week == None): week = 7
                events.append([year, int(week) + 1, [lat, lng]])
        
        events.sort(key=lambda x:(x[0], x[1]))
        
        return events

T4909 = TeamData("4909")

