from pathlib import Path
import os
import re
import metro
import pandas as pd

data_folder = Path('./data')
subfolders = [ f.path for f in os.scandir(data_folder) if (f.is_dir() and re.search('L12_Montparnasse_-_V',f.path)) ] # TODO : remove test

print("Number of trips : ",len(subfolders))

for trip in subfolders:
    trip_name = Path(trip).stem
    print() 
    print(trip_name)

    # Read data 
    df1 = pd.read_csv(Path(trip) / 'AccelerometerUncalibrated.csv')
    df2 = pd.read_csv(Path(trip) / 'Accelerometer.csv')

    # Invert the sign of Y accel if the trip name requires it
    if re.search("Yinv",trip_name):
        df1['y'] = -1*df1['y']
        df2['y'] = -1*df2['y']

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
                section = trip_stations[i] + "_" + trip_stations[i+1]
                print(section)
                filename1 = trip_date + "_AccelerometerUncalibrated.csv"
                filename2 = trip_date + "_Accelerometer.csv"
                i = i+1
                # creating a folder hierarchy such as L4 / Chatelet-Cite / 2024-04-05_17-21-10_AccelerometerUncalibrated.csv 
                filepath1 = data_folder / trip_line / section / filename1
                filepath2 = data_folder / trip_line / section / filename2
                filepath1.parent.mkdir(parents=True, exist_ok=True)  # create parent folder if doesn't exist
                df1[(df1['seconds_elapsed']>begin) & (df1['seconds_elapsed']<t_stop)].to_csv(filepath1,index=False)
                df2[(df2['seconds_elapsed']>begin) & (df2['seconds_elapsed']<t_stop)].to_csv(filepath2,index=False)
            if re.search("start",line): # switch to next section
                begin = float(line.split(' ')[0])
                
    else:
        print("No valid timestamps found")
