import requests
import json

class TBA:
    def get_data(self, query):
        base_url = "https://www.thebluealliance.com/api/v3"
        tba_api_key = "?X-TBA-Auth-Key=DvsksoiRgVhXfcnDqqiYkVV9Z73UKTYbbBg5r4UklkSsUOe9Hg9ZoVgz9m1HgPD9"
        url = base_url + query + tba_api_key
        response = requests.get(url)
        return json.loads(response.text)