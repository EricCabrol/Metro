from pathlib import Path
import plotly.graph_objects as go
import pandas as pd
from scipy.signal import filtfilt, butter
import re
from dateutil import parser

# TODO : unify with plot_all_decel.py or (better) with plot_trips_selection.py

# INIT

path = Path('./data/L4/Chatelet_Cite/')
files = path.glob('*_Accelerometer.csv')
fs = {"calibrated" : 50, "uncalibrated" : 400 } # Sampling frequencies (Hz)
# Filter parameters
N = 4 # filter order
Wn = 0.2 # (Hz) cutoff frequency
b, a = butter(N, Wn, 'low',fs=fs['calibrated']) # low pass filter 


def get_day(filename):
    match = re.search('(\d{4}-\d{2}-\d{2})_\d{2}-\d{2}-\d{2}',filename)
    return(match.group(1))

fig = go.Figure()

# plot accel on the Y axis
for file in files:
    print("Recording : ",file)
    filename = (Path(file)).stem
    day = parser.parse(get_day(filename))
    legend = day.strftime('%d %b %Y')    
    try:
        df = pd.read_csv(Path(file)) # rebuild Path object is required  (because file isn't one)
        df['time'] = df['time']-df['time'][0] # Reset initial time of the recording to 0
        fig.add_trace(go.Scatter(x = df['time']/1e9, y = filtfilt(b, a, df['y']), name = legend))
        # fig.add_trace(go.Scatter(x = df['time']/1e9, y = df['y'], name = file))
    except:
        print("Couldn't read "+file)

fig.update_layout(
    title = 'Paris Line 4 - from Châtelet to Cité',
    xaxis_title = "time (s)",
    yaxis_title = "acceleration (m/s^2)",    
    yaxis_range=[-2,2]
)

fig.show()