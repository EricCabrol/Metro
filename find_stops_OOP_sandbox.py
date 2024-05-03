import re
import unidecode

class Trip:

    def __init__(self,tripname) -> None:
        self.name = unidecode.unidecode(tripname)

    def get_line(self):
        try:
            line_number = re.match('^L\d+',self.name)
            return(line_number.group(0))
        except:
            print("Line number not found when processing "+self.name)

    def get_start(self):
        try:
            trip_start = re.search('^L\d+[-_]*([\w_]+)_-_',self.name)
            return(trip_start.group(1))
        except:
            print("Initial station not found when processing "+self.name)
            
    def get_end(self):
        try:
            trip_end = re.search('^L\d+[-_]*([\w_]+)_-_([\w_]+)_-_',self.name)
            return(trip_end.group(2))
        except:
            print("Terminal station not found when processing "+self.name)
    
    def get_date(self):
        try:
            trip_date = re.search('\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}',self.name)
            return(trip_date.group(0))
        except:
            print("Date not found when processing "+self.name)
    


trip = Trip('L4_Montparnasse_-_Reaumur_-_bag-2024-01-25_12-16-45')
# trip = Trip('L4_Montparnasse_-_St-Michel_-_bag-2024-01-25_12-16-45')
print(trip.get_line())
print(trip.get_start())
print(trip.get_end())
print(trip.get_date())
