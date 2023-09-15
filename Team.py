from ApiCalls import TBA
from geopy.geocoders import Nominatim
import math
import statistics
import constants

class TeamData():
    events = []

    def __init__(self, team):
        self.tba = TBA()
        self.geolocator = Nominatim(user_agent="MyApp")
        self.team = team
        self.location = self.get_location()
        self.events = self.get_events()

    def get_location(self):
        data = self.tba.get_data("/team/frc" + self.team)
        city_raw = data["city"]
        city = city_raw.split("/")[0]
        state = data["state_prov"]
        address = city + ", " + state
        location = self.geolocator.geocode(address, country_codes="US")
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

        return sum(weeks) / len(weeks), statistics.pstdev(weeks)

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

        return sum(distances) / len(distances), statistics.pstdev(distances) * 69

    def get_prefrence(self, event_num):
        avg_event, std_event = self.get_week_prefrence(event_num)
        avg_loc, std_loc = self.get_location_pref(event_num)

        event_coef = 1.96 * (std_event / (math.sqrt(len(constants.YEAR_RANGE) - len(constants.EXCLUDED_YEARS))))
        loc_coef = 1.96 * (std_loc / (math.sqrt(len(constants.YEAR_RANGE) - len(constants.EXCLUDED_YEARS))))

        min_event, max_event = (avg_event - event_coef), (avg_event + event_coef)
        max_loc = loc_coef * 2
        if(min_event <= 0):
            min_event = 1
        
        return [math.floor(min_event), math.ceil(max_event)], max_loc

    def get_predicted_events(self, weeks, max_dist):
        predicted_events = []
        for event in constants.EVENTS:
            if(event[1] >= weeks[0] and event[1] <= weeks[1]):
                distance = math.sqrt(math.pow(abs(event[2][0]) - abs(self.location[0]), 2) + math.pow(abs(event[2][1]) - abs(self.location[1]), 2))
                predicted_events.append([event[0], distance])
                # if(distance <= max_dist): predicted_events.append([event[0], distance])
        predicted_events.sort(key=lambda x:(x[1]))
        return predicted_events[0]


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

