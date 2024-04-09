import re


class Trip:
    def __init__(self,tripname) -> None:
        self.name = tripname
    def get_line(self):
        try:
            line_number = re.match('^L\d+',self.name)
            return(line_number.group(0))
        except:
            print("Line number not found when processing "+self.name)
    def get_start(self):
        try:
            line_number = re.match('^L\d+',self.name)
            return(line_number.group(0))
        except:
            print("Line number not found when processing "+self.name)
            

    


trip_1 = Trip('L4_Montparnasse_Reaumur_bag-2024-01-25_12-16-45')
print(trip_1.get_line())