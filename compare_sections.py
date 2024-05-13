from pathlib import Path
import glob
import plotly.graph_objects as go
import pandas as pd
from scipy.signal import filtfilt, butter



path = './data/L4/Chatelet_Cite/'
files = glob.glob(path + '*_Accelerometer.csv')
fs = {"calibrated" : 50, "uncalibrated" : 400 } # Sampling frequencies (Hz)
# Filter parameters
N = 4 # filter order
Wn = 0.2 # (Hz) cutoff frequency
b, a = butter(N, Wn, 'low',fs=fs['calibrated']) # low pass filter 

# TODO : unify this with plot_all_decel.py or (better) with plot_trips_selection.py

fig = go.Figure()

# plot accel on the Y axis
for file in files:
    print("Recording : ",file)
    try:
        df = pd.read_csv(Path(file)) # rebuild Path object is required  (because file isn't one)
        df['time'] = df['time']-df['time'][0] # Reset initial time of the recording to 0
        fig.add_trace(go.Scatter(x = df['time']/1e9, y = filtfilt(b, a, df['y']), name = file))
        fig.add_trace(go.Scatter(x = df['time']/1e9, y = df['y'], name = file))
    except:
        print("Couldn't read "+file)

fig.update_layout(yaxis_range=[-2,2])
fig.show()