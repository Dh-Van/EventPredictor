from ApiCalls import TBA
from geopy.geocoders import Nominatim
import math

class TeamData():
    events = []

    def __init__(self, team):
        self.tba = TBA()
        self.geolocator = Nominatim(user_agent="MyApp")
        self.team = team
        self.location = self.get_location()
        self.events = self.get_events()


    def get_location(self):
        city = self.tba.get_data("/team/frc" + str(self.team))["city"]
        location = self.geolocator.geocode(city)
        try:
            return [location.latitude, location.longitude]
        except:
            return [0, 0]
    

    def get_week_prefrence(self, event_num):
        weeks = []
        for event in self.events:
            try:
                weeks.append(event[event_num - 1][1])
            except:
                print("Out of bounds")


        return sum(weeks) / len(self.events)

    def get_location_pref(self, event_num):
        event_locations = []
        distances = []
        for event in self.events:
            try:
                if(event[event_num - 1][1] < 6):
                    event_locations.append(event[event_num - 1][2])
            except:
                print("Sadness")
        
        for l in event_locations:
            distances.append(
                math.sqrt(math.pow(abs(l[0]) - abs(self.location[0]), 2) + math.pow(abs(l[1]) - abs(self.location[1]), 2))
            )

        return (sum(distances) / len(distances)) * 69

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

        last_year = 2020
        curr_year = 2020
        temp = []
        filtered_events = []
        for event in events:
            curr_year = event[0]
            if(curr_year != last_year):
                last_year = curr_year
                filtered_events.append(temp.copy())
                temp.clear()

            temp.append(event)
        filtered_events.append(temp)
        
        return filtered_events