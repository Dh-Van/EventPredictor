import requests
import json
import statbotics
import constants

class TBA:
    def get_data(self, query: str):
        tba_api_key = constants.TBA_AUTH_HEADER + constants.TBA_API_KEY
        url = constants.TBA_API_URL + query + tba_api_key
        response = requests.get(url)
        return json.loads(response.text)

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