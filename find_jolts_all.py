# Objective : find the "jolts" of positive acceleration at the very end of the braking phase
# (same as find_jolts.py, but for a whole directory)

import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
import os
import re
from shutil import copy


data_folder = Path('./data')
# data_folder = Path('./data_test')

# subfolders = [ f.path for f in os.scandir(data_folder) if f.is_dir() ]
subfolders = [ f.path for f in os.scandir(data_folder) if (f.is_dir() and re.search('L4_Les_Halles',f.path)) ] # TEST


# INITIALISATION

fs_calibrated = 50 # (Hz) sampling frequency
min_amplitude_jolt = 1.5 # (m/s^2) minimum acceleration to consider the peak as a jolt 
min_amplitude_restart = 0.5 # (m/s^2) minimum acceleration to consider that the metro restarts 
min_stop_duration = 20 # (s) min duration before peak and restart 
nok_trips = [] # list of trips for which timestamps will require a manual validation

# LOOP ON TRIPS

for trip in subfolders:
    trip_name = Path(trip).stem
    print(trip_name)
    # if the timestamps have already been validated skip to next trip
    if os.path.exists(Path(trip) / "timestamps_valid.txt"):
        continue

    df = pd.read_csv(Path(trip) / 'Accelerometer.csv')
    df['time'] = df['time']-df['time'][0] # Reset initial time

    # Invert the sign of Y accel if the trip name requires it
    if re.search("Yinv",trip_name):
        df['y'] = -1*df['y']

    begin = 0 # init
    end = 0 # index init
    df['stop'] = 0 # initialize a new column, boolean like (True if metro stopped)
    stopped = False

    # WRITE TIMESTAMPS

    with open(Path(trip) / "timestamps.txt", mode="w") as output_file:
        output_file.write("Timestamps for trip "+trip+"\n")
        for ind in df.index:
            accel = df['y'][ind]
            if (accel > min_amplitude_jolt) :
                begin = ind
                stopped = True
            if stopped and (accel > min_amplitude_restart) and (ind-begin) > fs_calibrated*min_stop_duration:
                stopped = False
                end = ind
                df.loc[begin:end,'stop'] = 1
                output_file.write(str(df['time'][begin]/1e9)+" stop\n")
                output_file.write(str(df['time'][end]/1e9)+" start\n")

    # PLOT ACCEL AND TIMESTAMPS

    fig = go.Figure()

    fig.add_trace(go.Scatter(x = df['time']/1e9, y = df['y'], name = 'acceleration')) 
    fig.add_trace(go.Scatter(x = df['time']/1e9, y = df['stop'], name = 'stop')) 

    fig.update_layout(
        title="Calibrated acceleration and stops for trip "+trip_name,
        xaxis_title="time (s)",
        yaxis_title="acceleration (m/s^2)",
        yaxis_range=[-4,4]
    )

    fig.show()

    # ASK USER INPUT FOR CONFIRMATION

    valid = input("Are the timestamps OK ? (y/n) ")

    if re.match("[yY]",valid):
        copy(Path(trip) / "timestamps.txt",Path(trip) / "timestamps_valid.txt")
    else:
        nok_trips.append(trip_name)


print("List of NOK trips")
print(nok_trips)
