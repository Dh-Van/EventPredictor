import requests
import json
import statbotics
import constants
from geopy.geocoders import Nominatim

class TBA:
    def get_data(self, query: str):
        tba_api_key = constants.TBA_AUTH_HEADER + constants.TBA_API_KEY
        url = constants.TBA_API_URL + query + tba_api_key
        response = requests.get(url)
        return json.loads(response.text)

    def generate_2024_events(self):
        self.geolocator = Nominatim(user_agent="MyApp")
        events = self.get_data("/district/2024ne/events")
        output = []
        for e in events:
            city_raw = e["city"]
            city = city_raw.split("/")[0]
            state = e["state_prov"]
            address = city + ", " + state
            location = self.geolocator.geocode(address, country_codes="US")
            output.append([e["name"], e["week"], [location.latitude, location.longitude]])
        return output
    
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

class Statbotics:
    def __init__(self):
        self.sb = statbotics.Statbotics()

    def check_epa(self, team_number: str):
        try:
            metrics = self.sb.get_team(int(team_number))
            if(int(metrics["norm_epa"]) >= constants.MIN_NORM_EPA): return True
        except:
            print("invalid query")
            return False
        return False
    
t = TBA()
print(t.generate_2024_events())