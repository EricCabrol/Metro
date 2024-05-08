from pathlib import Path
import os
import re
import metro



data_folder = Path('./data')
subfolders = [ f.path for f in os.scandir(data_folder) if (f.is_dir() and re.search('L4_Les_Halles',f.path)) ] # TEST

print("Number of trips : ",len(subfolders))

for trip in subfolders:
    trip_name = Path(trip).stem
    print() 
    print(trip_name)
    timestamps_path = Path(trip) / "timestamps_valid.txt"
    # count the number of stops if the file exists
    if timestamps_path.is_file(): 
        filecontent = timestamps_path.read_text()
        nb_stops = len(re.findall('stop',filecontent))
        print("Number of stops found : ",nb_stops)

        tripObj = metro.Trip(trip_name)
        trip_stations = tripObj.get_stations()
        print(trip_stations)

        for i in range(1,nb_stops+1):
            print(i,trip_stations[i])
        print()
    else:
        print("No valid timestamps found")

