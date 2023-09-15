import requests
import json
import statbotics

class TBA:
    def get_data(self, query):
        base_url = "https://www.thebluealliance.com/api/v3"
        tba_api_key = "?X-TBA-Auth-Key=DvsksoiRgVhXfcnDqqiYkVV9Z73UKTYbbBg5r4UklkSsUOe9Hg9ZoVgz9m1HgPD9"
        url = base_url + query + tba_api_key
        response = requests.get(url)
        return json.loads(response.text)

class Statbotics:
    def __init__(self):
        self.sb = statbotics.Statbotics()

    def check_epa(self, MAX_EPA, team_number):
        try:
            metrics = self.sb.get_team(team_number)
        except:
            print("invalid query")
            return False
        if(int(metrics["norm_epa"]) >= MAX_EPA):
            return True
        return False