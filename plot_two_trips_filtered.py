import pandas as pd
import plotly.graph_objects as go
import numpy as np
from scipy.signal import filtfilt, butter


# Comparison of two trips - Filtered calibrated accelerations

data_folder = './data/'
trip_1 = 'L4_Montparnasse_Reaumur_bag-2024-01-25_12-16-45'
trip_2 = 'L13_Champs_Pernety_bag-2024-01-25_18-41-33'

# Filter parameters
N = 4
Wn = 2 # low-pass frequency
b, a = butter(N, Wn, 'low',fs=50) # Calibrated accel is sampled at 50 Hz

 
fig = go.Figure()

# L4 filtered 

df = pd.read_csv(data_folder+trip_1+'/Accelerometer.csv')
df['time'] = df['time']-df['time'][0]
df_sel = df[df['time']<600e9] # Caution : selection of a time window
fig.add_trace(go.Scatter(x = df_sel['time']/1e9, y = filtfilt(b, a, df_sel['y']), name = 'L4 filt. '+str(Wn)+' Hz')) 

# not filtered
# fig.add_trace(go.Scatter(x = df_sel['time']/1e9, y = df_sel['y'], name = 'L4 not filtered')) 

# L13 filtered

df = pd.read_csv(data_folder+trip_2+'/Accelerometer.csv')
df['time'] = df['time']-df['time'][0]
df_sel = df[df['time']<600e9]
fig.add_trace(go.Scatter(x = df_sel['time']/1e9, y = filtfilt(b, a, df_sel['y']), name = 'L13 filt. '+str(Wn)+' Hz')) 


fig.update_layout(
    title="Comparison of metro lines 4 and 13",
    xaxis_title="time (s)",
    yaxis_title="acceleration (m/s^2)",

)

fig.show()
