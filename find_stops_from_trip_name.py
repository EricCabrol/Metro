import re
import os
import unidecode
from difflib import SequenceMatcher

folder = './data'
# Find the trips subdirectories starting by a L in ./data
trips = [ f.name for f in os.scandir(folder) if f.is_dir() and f.name.startswith('L')]

stations = {
    'L3' : ('Saint-Lazare','Havre-Caumartin','Opera','Quatre-Septembre','Bourse','Sentier','Reaumur'),
    'L4' : ('Montparnasse','St-Placide','St-Sulpice','St-Germain','Odeon','St-Michel','Cite','Chatelet','Les Halles','Etienne Marcel','Reaumur'),
    'L6' : ('Dupleix','La Motte','Cambronne','Sevres-Lecourbe','Pasteur','Montparnasse','Edgar Quinet','Raspail'),
    'L8' : ('La Motte','Ecole Militaire','La Tour-Maubourg','Invalides','Concorde','Madeleine'),
    'L12' : ('Montparnasse','Falguiere','Pasteur','Volontaires'),
    'L13' : ('Pernety','Gaite','Montparnasse','Duroc','St Francois Xavier','Varenne','Invalides','Champs-Elysees','Miromesnil','St-Lazare')
}

# ('Montparnasse','Reaumur','Odeon','Dupleix','Madeleine','Volontaires','Raspail','Pasteur','Les Halles','Duroc')

for trip in trips:
    print(trip)
    line = re.search('^(L\d+)',unidecode.unidecode(trip)).group(1)
    print(line)
    # Does the start identified matches exactly one of the line stations ?
    match = re.search('^L\d+[-_]*([\w_]+)_-_',unidecode.unidecode(trip))
    if match is not None:
        start = re.search('^L\d+[-_]*([\w_]+)_-_',unidecode.unidecode(trip)).group(1)
        if start in stations[line]:
            print(start)
        else:
            for station in stations[line]:
                s = SequenceMatcher(None,start, station)
                if s.ratio()>0.8:
                    print(station,s.ratio())                
            # print('Start not found for trip ',trip)

    # Does the start identified matches approximately one of the line stations ?
    # except:
    #     start = re.search('^L\d+[-_]*([\w_]+)_-_',unidecode.unidecode(trip)).group(1)
    #     for station in stations[line]:
    #         s = SequenceMatcher(None, "St-Placide", station)
    #         print(station,s.ratio())

    # for station in stations_L4:
    #     found_start = re.search('^L\d+[-_]*'+station,trip)
    #     if (found_start):
    #         kept_station = station
    #         print(kept_station)

    print()