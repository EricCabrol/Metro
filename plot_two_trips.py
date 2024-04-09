import pandas as pd
import plotly.graph_objects as go

# Comparison of two trips - No filter

data_folder = './data/'
trip_1 = 'L4_Montparnasse_-_Reaumur_bag-2024-01-25_12-16-45'
trip_2 = 'L13_Champs_-_Pernety_bag-2024-01-25_18-41-33'

# Caution : possible selection of a time window + addition of offset

# UNCALIBRATED DATA

fig = go.Figure()

df = pd.read_csv(data_folder+trip_1+'/AccelerometerUncalibrated.csv')
df['time'] = df['time']-df['time'][0]
# df_sel = df[df['time']<420e9]
offset = 0
fig.add_trace(go.Scatter(x = df['time']/1e9, y = df['y']+offset, name = 'L4')) 

df = pd.read_csv(data_folder+trip_2+'/AccelerometerUncalibrated.csv')
df['time'] = df['time']-df['time'][0]
# df_sel = df[df['time']<420e9]
offset = 0
fig.add_trace(go.Scatter(x = df['time']/1e9, y = df['y']+offset, name = 'L13')) 

fig.update_layout(
    title="Comparison of metro lines 4 and 13",
    xaxis_title="time (s)",
    yaxis_title="uncalibrated acceleration (m/s^2)",
    yaxis_range=[-4,4]
)
fig.show()



# CALIBRATED DATA

fig = go.Figure()

df = pd.read_csv(data_folder+trip_1+'/Accelerometer.csv')
df['time'] = df['time']-df['time'][0]
# df_sel = df[df['time']<420e9]
offset = 0.
fig.add_trace(go.Scatter(x = df['time']/1e9, y = df['y']+offset, name = 'L4')) 

df = pd.read_csv(data_folder+trip_2+'/Accelerometer.csv')
df['time'] = df['time']-df['time'][0]
# df_sel = df[df['time']<420e9]
offset = 0.
fig.add_trace(go.Scatter(x = df['time']/1e9, y = df['y']+offset, name = 'L13')) 

fig.update_layout(
    title="Comparison of metro lines 4 and 13",
    xaxis_title="time (s)",
    yaxis_title="calibrated acceleration (m/s^2)",
    yaxis_range=[-4,4]
)
fig.show()