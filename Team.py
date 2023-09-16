from ApiCalls import TBA
from geopy.geocoders import Nominatim
import math
import statistics
import constants
from scipy.stats import norm

class TeamData():
    events = []

    def __init__(self, team):
        self.tba = TBA()
        self.geolocator = Nominatim(user_agent="MyApp")
        self.team = team
        self.location = self.get_location()
        self.events = self.get_events()

    def get_mean_std(self, event_num):
        data = self.get_event_loc_pref(self.events, event_num)
        return data
        
    def get_prefrence(self, event_num):
        earliest_events = []
        latest_events = []
        prefrences = []
        avg_week, avg_dist = self.get_event_loc_pref(self.events, event_num)
        chance_prev_week = 1 - (avg_week % 1)
        chance_next_week = (avg_week % 1)
        for event in constants.EVENTS:
            event_week = event[1] + 1
            event_distance = math.sqrt(math.pow(abs(event[2][0]) - abs(self.location[0]), 2) + math.pow(abs(event[2][1]) - abs(self.location[1]), 2)) * 69
            e = event.copy()
            e.append(event_distance)

            if(event_week == math.floor(avg_week)):
                earliest_events.append(e)
            elif(event_week == math.ceil(avg_week)):
                latest_events.append(e)

        earliest_events.sort(key=lambda x:(x[3]))
        latest_events.sort(key=lambda x:(x[3]))
        
        if(chance_prev_week >= chance_next_week):
            prev_counter = 0
            lat_counter = 0
            for i in range(len(earliest_events) + len(latest_events)):
                if(prev_counter < len(earliest_events) and earliest_events[prev_counter][3] <= avg_dist):
                    prefrences.append(earliest_events[prev_counter])
                    prev_counter += 1
                    continue
                elif(lat_counter < len(latest_events) and latest_events[lat_counter][3] <= avg_dist):
                    prefrences.append(latest_events[lat_counter])
                    lat_counter += 1
                    continue
                elif(prev_counter < len(earliest_events)):
                    prefrences.append(earliest_events[prev_counter])
                    prev_counter += 1
                    continue
                elif(lat_counter < len(latest_events)):
                    prefrences.append(latest_events[lat_counter])
                    lat_counter += 1
                    continue

        if(chance_next_week > chance_prev_week):
            prev_counter = 0
            lat_counter = 0
            for i in range(len(earliest_events) + len(latest_events)):
                if(lat_counter < len(latest_events) and latest_events[lat_counter][3] <= avg_dist):
                    prefrences.append(latest_events[lat_counter])
                    lat_counter += 1
                    continue
                elif(prev_counter < len(earliest_events) and earliest_events[prev_counter][3] <= avg_dist):
                    prefrences.append(earliest_events[prev_counter])
                    prev_counter += 1
                    continue
                elif(lat_counter < len(latest_events)):
                    prefrences.append(latest_events[lat_counter])
                    lat_counter += 1
                    continue
                elif(prev_counter < len(earliest_events)):
                    prefrences.append(earliest_events[prev_counter])
                    prev_counter += 1
                    continue
        codes = []
        for e in prefrences:
            codes.append(e[0])
        return codes
    
    def get_prob(data, lower, upper):
        upper_limit = norm(loc = data[0], scale = data[1]).cdf(upper)
        lower_limit = norm(loc = data[0], scale = data[1]).cdf(lower)
        prob = upper_limit - lower_limit
        if(prob < 0.001): prob = 0
        return prob

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
    
    def get_event_loc_pref(self, events, event_num):
        event_weeks = []
        distances = []

        for event in events:
            try:
                event_weeks.append(event[event_num - 1][1])
                event_loc = event[event_num - 1][2]
                distances.append(
                    math.sqrt(math.pow(abs(event_loc[0]) - abs(self.location[0]), 2) + math.pow(abs(event_loc[1]) - abs(self.location[1]), 2)) * 69
                )
            except:
                print("Error in get_event_loc_pref")
                return 0, 0
        return [statistics.mean(event_weeks), statistics.pstdev(event_weeks)], [statistics.mean(distances), statistics.pstdev(distances)]    

    def get_events(self):
        event_data = self.tba.get_data("/team/frc" + self.team + "/events")
        events = []

        for year in range(constants.YEAR_RANGE[0], constants.YEAR_RANGE[1] + 1): events.append([])

        for event in event_data:
            week = event["week"]
            if(week == None): week = 7
            year = int(event["year"])
            if(event["event_type"] <= 1 and year >= constants.YEAR_RANGE[0] and constants.EXCLUDED_YEARS.count(year) == 0):
                lat = float(event["lat"])
                lng = float(event["lng"])
                index = year - constants.YEAR_RANGE[0]
                events[index].append([year, int(week) + 1, [lat, lng]])

        events = list(filter(None, events))
        for e in events:
            e.sort(key=lambda x:(x[0], x[1]))
        return events