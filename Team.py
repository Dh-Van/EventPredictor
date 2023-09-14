from ApiCalls import TBA

class TeamData():
    events = []

    def __init__(self, team):
        self.tba = TBA()
        self.team = team
        self.events = self.get_events()
        # print(self.events)

    def get_week_prefrence(self, event_num):
        weeks = []
        l = len(self.events)
        for event in self.events:
            try:
                weeks.append(event[event_num - 1][1])
            except:
                print("Out of bounds")

        return sum(weeks) / len(self.events)

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

