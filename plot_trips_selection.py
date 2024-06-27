import pandas as pd
import plotly.graph_objects as go
import numpy as np
from scipy.signal import filtfilt, butter
from pathlib import Path
import metro 


# User selection

data_folder = Path('./data_test')
trips = ('L4_Etienne_Marcel_-_Montparnasse_-_brutal_2_stops_annotated-2024-06-24_17-22-44','dummy')

# Do we plot calibrated, uncalibrated, filtered or unfiltered data ? 

calib_choices = {"calibrated":True,"uncalibrated":False}
filter_choices = {"filtered":False,"unfiltered":True}

t_max = 900 # (s) can be used to truncate the trips (to reduce processing time)

# Parameters below shouldn't change for a given smartphone / SensorLogger configuration

accel_files = {"calibrated":"Accelerometer.csv","uncalibrated":"AccelerometerUncalibrated.csv"}

# Filter parameters
N = 4 # filter order
Wn = 2 # (Hz) cutoff frequency

fig = go.Figure()

for trip in trips:

    for calib_key in calib_choices.keys(): 
        if calib_choices[calib_key] is True:
            try:
                df = pd.read_csv(data_folder / trip / accel_files[calib_key])
            except:
                print(accel_files[calib_key]+" not found for trip "+trip)
                continue
            try: # Extract sampling frequency from the record
                record = metro.Record(data_folder / trip / accel_files[calib_key])
                sampling_frequency = record.get_frequency()
                print('Identified sampling frequency = '+sampling_frequency+' for trip'+trip)
            except:
                print('could not identify sampling frequency for trip '+trip)
            
            df['time'] = df['time']-df['time'][0] # Here we choose to reset t0 to 0
            df = df[df['time'] < t_max*1e9] # Truncate to t_max and convert to ns
            # Plotting filtered and/or unfiltered 
            if filter_choices['unfiltered'] is True:
                fig.add_trace(go.Scatter(x = df['time']/1e9, y = df['y'], name = trip+' '+calib_key))
            if filter_choices['filtered'] is True:
                b, a = butter(N, Wn, 'low',fs=sampling_frequency) # using identified sampling frequency
                fig.add_trace(go.Scatter(x = df['time']/1e9, y = filtfilt(b, a, df['y']), name = trip+' '+calib_key+' filt. '+str(Wn)+' Hz')) 

fig.update_layout(
    title = '  VS  '.join([x for x in trips]),
    xaxis_title = "time (s)",
    yaxis_title = "acceleration (m/s^2)",
    yaxis_range=[-4,4]
)

fig.show()
