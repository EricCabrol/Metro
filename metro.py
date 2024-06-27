import re
import unidecode
from difflib import SequenceMatcher
import numpy as np
import pandas as pd


class Record:

    def __init__(self,file) -> None:
        self.file = file

    def get_frequency(self): # returns frequency of a csv file recorded with SensorLogger
        try:
            df = pd.read_csv(self.file)
            sampling_rate = 1 / np.diff(df['seconds_elapsed'])
            return(np.mean(sampling_rate))
        except:
            print("Could not compute sample time for file "+self.file)      




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
            bits = self.name.split('_-',2)
            trip_start = re.search('^L\d+_*-*(.+)',bits[0]) # matches L4_station or L4-station or L4_-station
            return(re.sub('_',' ',trip_start.group(1))) # replaces underscores by spaces inside station names (ex : "Les Halles")
        except:
            print("Initial station not found when processing "+self.name)
            
    def get_end(self):
        try:
            bits = self.name.split('_-',2)
            trip_end = re.sub('^_','',bits[1])
            return(trip_end)
        except:
            print("Terminal station not found when processing "+self.name)
    
    def get_date(self):
        try:
            trip_date = re.search('\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}',self.name)
            return(trip_date.group(0))
        except:
            print("Date not found when processing "+self.name)

    def get_stations(self): # TODO : work in progress
        stations = {
        'L3' : ['Europe','St-Lazare','Havre-Caumartin','Opera','Quatre-Septembre','Bourse','Sentier','Reaumur'],
        'L4' : ['Montparnasse','St-Placide','St-Sulpice','St-Germain','Odeon','St-Michel','Cite','Chatelet','Les Halles','Etienne Marcel','Reaumur'],
        'L6' : ['Dupleix','La Motte','Cambronne','Sevres-Lecourbe','Pasteur','Montparnasse','Edgar Quinet','Raspail'],
        'L8' : ['La Motte','Ecole Militaire','La Tour-Maubourg','Invalides','Concorde','Madeleine'],
        'L12' : ['Montparnasse','Falguiere','Pasteur','Volontaires'],
        'L13' : ['Pernety','Gaite','Montparnasse','Duroc','St-Francois-Xavier','Varenne','Invalides','Champs-Elysees','Miromesnil','St-Lazare']
        }
        try:
            trip_start = self.get_start()
            trip_end = self.get_end()
            trip_line = self.get_line()
            line_stations = stations[trip_line] # only to improve readability 
            # in case of mistyping, replace by a close enough match
            if (trip_start not in line_stations):
                print('First station identified from regexp : ',trip_start)
                max_match = 0
                for station in line_stations:
                    s = SequenceMatcher(None,trip_start, station)
                    if s.ratio() > max_match:
                        kept = station
                        max_match = s.ratio()
                trip_start = kept
                print('First station is likely to be : ', trip_start)
                if max_match < 0.8 : # arbitrary threshold, works quite well
                    print ('Warning ! Confidence threshold too low : ', max_match)
            # if the trip is in the same direction as the line definition
            if (line_stations.index(trip_start) < line_stations.index(trip_end)):
                # return the corresponding slice of the line stations, including the end
                # (add 1 to get the last station)
                return(line_stations[line_stations.index(trip_start):line_stations.index(trip_end)+1]) 
            else:  # do the opposite :)
                tmp = line_stations[line_stations.index(trip_start):line_stations.index(trip_end):-1]
                # ugly hack to get the first station (couldn't find a better way)
                tmp.append(line_stations[line_stations.index(trip_end)]) 
                return(tmp)
        except:
            print("Could not retrieve stops for "+self.name)

if __name__=='__main__':

    trip_list = ['L3_Sentir_-_St-Lazare_-2024-05-03_17-04-03']
    for t in trip_list:
        print(t)
        trip = Trip(t)
        print(trip.get_line())
        print(trip.get_start())
        print(trip.get_end())
        print(trip.get_date())
        print(trip.get_stations())
        print()
