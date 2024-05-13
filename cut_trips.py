from pathlib import Path
import os
import re
import metro
import pandas as pd

data_folder = Path('./data')
subfolders = [ f.path for f in os.scandir(data_folder) if (f.is_dir() and re.search('L4_Les_Halles.+leg',f.path)) ] # TEST

print("Number of trips : ",len(subfolders))

for trip in subfolders:
    trip_name = Path(trip).stem
    print() 
    print(trip_name)

    # Read data 
    df = pd.read_csv(Path(trip) / 'AccelerometerUncalibrated.csv')

    # Get trip attributes
    tripObj = metro.Trip(trip_name)
    trip_stations = tripObj.get_stations()
    trip_line = tripObj.get_line()
    trip_date = tripObj.get_date()
 
    timestamps_path = Path(trip) / "timestamps_valid.txt"
    # count the number of stops if the file exists
    if timestamps_path.is_file(): 
        with open(timestamps_path) as f:
            lines = f.readlines()
        begin = 0
        i = 0
        for line in lines:
            if re.search("stop",line):
                t_stop = float(line.split(' ')[0])
                # section_filename = trip_line + "_" + trip_stations[i] + "_" + trip_stations[i+1] + "_" + trip_date
                section = trip_stations[i] + "_" + trip_stations[i+1]
                filename = trip_date + ".csv"
                print(section)
                i = i+1
                # print(df[(df['time']>begin*1e9) & (df['time']<t_stop*1e9)].head(3))
                # print()
                # print(df[(df['time']>begin*1e9) & (df['time']<t_stop*1e9)].tail(3))
                # print()
                filepath = data_folder / trip_line / section / filename
                filepath.parent.mkdir(parents=True, exist_ok=True)  # create parent folder if doesn't exist
                df[(df['seconds_elapsed']>begin) & (df['seconds_elapsed']<t_stop)].to_csv(filepath,index=False)
            if re.search("start",line):
                begin = float(line.split(' ')[0])
                
    else:
        print("No valid timestamps found")
