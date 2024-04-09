import pandas as pd
import plotly.graph_objects as go

data_folder = './data/'
trip_1 = 'L4_Montparnasse_Reaumur_bag-2024-01-25_12-16-45'

# Caution : selection of a time window
fig = go.Figure()

df = pd.read_csv(data_folder+trip_1+'/AccelerometerUncalibrated.csv')
df['time'] = df['time']-df['time'][0]
df_sel = df[df['time']<420e9]
fig.add_trace(go.Scatter(x = df_sel['time']/1e9, y = df['y'], name = 'uncalibrated')) 

df = pd.read_csv(data_folder+trip_1+'/Accelerometer.csv')
df['time'] = df['time']-df['time'][0]
df_sel = df[df['time']<420e9]
fig.add_trace(go.Scatter(x = df_sel['time']/1e9, y = df['y'], name = 'calibrated')) 

fig.update_layout(
    title="Comparison of uncalibrated and calibrated Android data",
    xaxis_title="time (s)",
    yaxis_title="acceleration (m/s^2)",

)

fig.show()