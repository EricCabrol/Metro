import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

p = Path('./data')
trip_1 = 'L4_Montparnasse_-_Reaumur_bag-2024-01-25_12-16-45'

t_max = 500 # max time (s)

fig = go.Figure()

df = pd.read_csv(p / trip_1 / 'AccelerometerUncalibrated.csv')
df['time'] = df['time']-df['time'][0]
df = df[df['time']<t_max*1e9]           
fig.add_trace(go.Scatter(x = df['time']/1e9, y = df['y'], name = 'uncalibrated')) 

df = pd.read_csv(p / trip_1 / 'Accelerometer.csv')
df['time'] = df['time']-df['time'][0]
df = df[df['time']<t_max*1e9]           
fig.add_trace(go.Scatter(x = df['time']/1e9, y = df['y'], name = 'calibrated')) 

fig.update_layout(
    title="Comparison of uncalibrated and calibrated Android data",
    xaxis_title="time (s)",
    yaxis_title="acceleration (m/s^2)",
    yaxis_range=[-4,4]

)

fig.show()