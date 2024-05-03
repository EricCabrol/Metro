import pandas as pd
import plotly.graph_objects as go
import numpy as np
from scipy.signal import filtfilt, butter
from pathlib import Path


# User selection

trips = ('L4_Montparnasse_-_Reaumur_-_soft-2024-03-29_08-07-51',
         'L4_Montparnasse_-_Reaumur_bag-2024-01-25_12-16-45')

calib_choices = {"calibrated":True,"uncalibrated":False}
filter_choices = {"filtered":True,"unfiltered":False}

t_max = 900 # (s) can be used to truncate the trips (to reduce processing time)

# Parameters below shouldn't change for a given smartphone / SensorLogger configuration

data_folder = Path('./data')
accel_files = {"calibrated":"Accelerometer.csv","uncalibrated":"AccelerometerUncalibrated.csv"}
fs = {"calibrated" : 50, "uncalibrated" : 400 } # Sampling frequencies (Hz)

# Filter parameters
N = 4 # filter order
Wn = 2 # (Hz) cutoff frequency

fig = go.Figure()

for trip in trips:

    for calib_key in calib_choices.keys():
        if calib_choices[calib_key] is True:
            df = pd.read_csv(data_folder / trip / accel_files[calib_key])
            df['time'] = df['time']-df['time'][0]
            df = df[df['time'] < t_max*1e9] # Conversion to ns
            if filter_choices['unfiltered'] is True:
                fig.add_trace(go.Scatter(x = df['time']/1e9, y = df['y'], name = trip+' '+calib_key))
            if filter_choices['filtered'] is True:
                b, a = butter(N, Wn, 'low',fs=fs[calib_key]) # low pass filter with the proper cutoff frequency
                fig.add_trace(go.Scatter(x = df['time']/1e9, y = filtfilt(b, a, df['y']), name = trip+' '+calib_key+' filt. '+str(Wn)+' Hz')) 

fig.update_layout(
    title = '  VS  '.join([x for x in trips]),
    xaxis_title = "time (s)",
    yaxis_title = "acceleration (m/s^2)",
    yaxis_range=[-4,4]
)

fig.show()
