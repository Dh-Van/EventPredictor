from ApiCalls import TBA
from ApiCalls import Statbotics
from Team import TeamData
import constants

class DistrictData():

    def __init__(self):
        self.tba = TBA()
        self.sb = Statbotics()
        # file = ""
        # teams = self.tba.get_data("/district/2023ne/teams")

    def get_event_prefrences(self, event_num, team_list):
        prefrences = ""
        counter, total = 0, len(team_list)

        for team in team_list:
            print(str(total - counter) + " teams left")
            curr_team = TeamData(str(team))
            data = curr_team.get_prefrence(event_num)
            prefrences += str(team) + ", " + str(data[0][0]) + ", " + str(data[0][1]) + ", " + str(data[1]) + "\n"
            counter += 1

        file_name = ""
        if(event_num == 1): 
            file_name += "First" 
        else: 
            file_name += "Second"
        self.write_to_file(file_name + "_Event_Data.txt", prefrences)

    def write_to_file(self, file_name, text):
        f = open(file_name, "w")
        f.write(text)
        f.close()


New_England = DistrictData()
New_England.get_event_prefrences(1, constants.TEN_TEAMS)