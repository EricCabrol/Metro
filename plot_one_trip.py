import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

p = Path('./data')
trip_1 = 'L4_Montparnasse_-_Reaumur_bag-2024-01-25_12-16-45'
file = 'Accelerometer.csv'

t_max = 500 # max time (s)

# CALIBRATED DATA

df = pd.read_csv(p / trip_1 / file)
df['time'] = df['time']-df['time'][0]   # reset t0
df = df[df['time']<t_max*1e9]           # time window selection

fig = go.Figure()
fig.add_trace(go.Scatter(x = df['time']/1e9, y = df['y'], name = 'L4')) 
fig.update_layout(
    title="L4 Montparnasse Reaumur 25 Jan 2024",
    xaxis_title="time (s)",
    yaxis_title="calibrated acceleration (m/s^2)",
    yaxis_range=[-4,4]
)
fig.show()

# UNCALIBRATED DATA


df = pd.read_csv(data_folder+trip_1+'/AccelerometerUncalibrated.csv')
df['time'] = df['time']-df['time'][0]
df = df[df['time']<t_max*1e9]

fig = go.Figure()
fig.add_trace(go.Scatter(x = df['time']/1e9, y = df['y'], name = 'L4')) 
fig.update_layout(
    title="L4 Montparnasse Reaumur 25 Jan 2024",
    xaxis_title="time (s)",
    yaxis_title="uncalibrated acceleration (m/s^2)",
    yaxis_range=[-4,4]
)
fig.show()



