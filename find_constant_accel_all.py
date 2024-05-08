# Objective : find the time windows of constant acceleration to identify the stops
# (same as find_constant_accel.py, but for a whole directory)
# Process uncalibrated data, since calibrated accel is not constant when the metro is stopped ... 

import pandas as pd
import plotly.graph_objects as go
from scipy.signal import filtfilt, butter
from pathlib import Path
import os
import re 
from shutil import copy
import metro


data_folder = Path('./data')

# subfolders = [ f.path for f in os.scandir(data_folder) if f.is_dir() ]
subfolders = [ f.path for f in os.scandir(data_folder) if (f.is_dir() and re.search('L4_Les_Halles',f.path)) ] # TEST
# subfolders = [ f.path for f in os.scandir(data_folder) if (f.is_dir() and re.search('L3',f.path)) ] # TEST

# INITIALISATION

fs_uncalibrated = 400 # acceleration sampling frequency
tol = 0.15 # tolerance to consider the signal constant (m/s^2)
min_stop_duration = 15 # minimum time window (s)
nok_trips = [] # list of trips for which timestamps will require a manual validation

# Filter parameters
N = 4 # order of the filter
Wn = 1 # cutoff frequency
# b1, a1 = butter(N, Wn, 'low',fs=50) # Calibrated accel is sampled at 50 Hz
b2, a2 = butter(N, Wn, 'low',fs=fs_uncalibrated) # Uncalibrated accel is sampled at 400 Hz

# LOOP ON TRIPS

for trip in subfolders:
    trip_name = Path(trip).stem
    print("\n"+trip_name)
    # if the timestamps have already been validated skip to next trip
    if os.path.exists(Path(trip) / "timestamps_valid.txt"):
        continue

    df = pd.read_csv(Path(trip) / 'AccelerometerUncalibrated.csv')
    df['time'] = df['time']-df['time'][0] # Reset initial time

    # Invert the sign of Y accel if the trip name requires it
    if re.search("Yinv",trip_name):
        df['y'] = -1*df['y']
    
    # Add a filtered column
    df['y_filt'] = filtfilt(b2, a2, df['y']) 

    # INITIALISATION
    tmp = 0 # accel init
    begin = 0 # init
    end = 0 # index init
    df['stop'] = 0 # initialize a new column, boolean like (True if metro stopped)
    avg = 0 # (m/s^2) average acceleration when stopped (relevant only for uncalibrated data)
    t_stops = [] # list of timestamps at the beginning of each stop

    # IDENTIFICATION OF STOPS
    with open(Path(trip) / "timestamps.txt", mode="w") as output_file:
        output_file.write("Timestamps for trip "+trip_name+"\n")

        for ind in df.index:
            if abs(df['y_filt'][ind]-tmp) < tol: # working on filtered acceleration
                end = ind
            else:
                if (end-begin) > fs_uncalibrated*min_stop_duration:
                    df.loc[begin:end,'stop'] = 1 
                    t_stops.append(df['time'][begin]/1e9)
                    output_file.write(str(df['time'][begin]/1e9)+" stop\n")
                    output_file.write(str(df['time'][end]/1e9)+" start\n")

                # reinitialize index and value at the beginning of the window
                begin = ind
                tmp = df['y_filt'][ind]
        # Write the last time step
        output_file.write(str(df['time'].iloc[-1]/1e9)+" end\n")
        # Write avg acceleration
        output_file.write(str(df[df['stop']==1]['y_filt'].mean())+" avg accel")

    # LIST TRIP STATIONS
    tripObj = metro.Trip(trip_name)
    trip_stations = tripObj.get_stations()
    print(trip_stations)
    # CAUTION : we may have a different number of stop names vs identified stops
    # With the method of constant accel, the number of stops should equal the number of trip_stations minus 2
    try:
        delta = len(trip_stations)-2-len(t_stops)
        if delta < 0:
            print("More stops identified than required")
            annotations = trip_stations[1:-1] + ['XXX']*-delta # for plotting only, see below
            print("Annotations ",annotations)
        if delta > 0:
            print("Less stops identified than required")
            annotations = trip_stations[1:-1-delta]
    except:
        print("Error when processing delta")

    #PLOT
    fig = go.Figure()
    fig.add_trace(go.Scatter(x = df['time']/1e9, y = df['y'], name = 'uncalibrated')) 
    fig.add_trace(go.Scatter(x = df['time']/1e9, y = filtfilt(b2, a2, df['y']), name = 'uncalibrated filtered')) 
    fig.add_trace(go.Scatter(x = df['time']/1e9, y = df['stop'], name = 'stop'))
    # Plot stop names
    try:
        for i,t in enumerate(t_stops):
            fig.add_annotation(x=t,y=0,text=annotations[i])
    except:
        print("Could not add annotations")
    # Plot and axis titles
    fig.update_layout(
        title="Uncalibrated accel for trip "+trip_name,
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

print("\nList of NOK trips")
print(nok_trips)
