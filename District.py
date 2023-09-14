from ApiCalls import TBA
from ApiCalls import Statbotics
from Team import TeamData

class DistrictData():

    premade_list = [
        1100, 125, 133, 1519, 1757, 176, 1768, 177, 195, 230, 319, 3205, 3467, 4909, 5687, 6328, 6329, 7407, 8013, 8046, 8085, 88, 95
    ]

    def __init__(self):
        self.tba = TBA()
        self.sb = Statbotics()
        file = ""
        teams = self.tba.get_data("/district/2023ne/teams")
        counter = 0
        c = len(teams)
        # team_list = []
        # for team in teams:
        #     print(str(c - counter) + " teams left")
        #     team_number = team["team_number"]
        #     if(not self.sb.check_epa(1658, team_number)): 
        #         counter += 1
        #         continue
        #     team_list.append(team_number)
        #     counter += 1

        counter = 0
        c = len(self.premade_list)
        for team in self.premade_list:
            print(str(c - counter) + " teams left")
            temp_team = TeamData(str(team))
            w1_pref = temp_team.get_week_prefrence(1)
            loc_pref = temp_team.get_location_pref(1)
            s = "" + str(team) + ", " + str(w1_pref) + ", " + str(loc_pref) + "\n"
            file += s
            counter += 1

        f = open("data.txt", "a")
        f.write(file)
        f.close()


New_England = DistrictData()
