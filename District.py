from ApiCalls import TBA
from ApiCalls import Statbotics
from Team import TeamData

class DistrictData():
    def __init__(self):
        self.tba = TBA()
        self.sb = Statbotics()
        file = ""
        teams = self.tba.get_data("/district/2023ne/teams")
        counter = 0
        c = len(teams)
        for team in teams:
            print(str(counter - c) + "teams left")
            team_number = team["team_number"]
            if(not self.sb.check_epa(1500, team_number)): 
                counter += 1
                continue
            temp_team = TeamData(str(team_number))
            w1_pref = temp_team.get_week_prefrence(1)
            s = "" + str(team_number) + ", " + str(w1_pref) + "\n"
            file += s
            counter += 1

        f = open("data.txt", "a")
        f.write(file)
        f.close()


New_England = DistrictData()
