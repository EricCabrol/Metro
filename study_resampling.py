import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
from scipy.signal import filtfilt, butter



data_folder = Path('./data')

trip_1 = 'L4_Montparnasse_-_Reaumur_-_bag-2024-01-25_12-16-45'

# df = pd.read_csv(data_folder / trip_1 / 'AccelerometerUncalibrated.csv', parse_dates=['time'],index_col='time')
df = pd.read_csv(data_folder / trip_1 / 'AccelerometerUncalibrated.csv')
# sampling_rate = 1 / np.diff(df['seconds_elapsed'])
# plt.hist(sampling_rate)
# plt.show()


df['DateTime'] = pd.DatetimeIndex(df['time'])
df = df.set_index('DateTime')
# print(df.head())

# Plot different resampling frequencies

fig = go.Figure()
fig.add_trace(go.Scatter(x = df.index, y = df['y'], name = 'initial signal')) 

for timestep in ('2.5ms','5ms','10ms','20ms','50ms','100ms'):
    print(timestep)
    df_res = df[['y']].resample(timestep).mean()
    
    fig.add_trace(go.Scatter(x = df_res.index, y = df_res['y'], name = timestep)) 

fig.update_layout(
    title="Comparison of resampling with different sampling frequencies "+trip_1,
    xaxis_title="time (s)",
    yaxis_title="acceleration (m/s^2)",
    yaxis_range=[-3,3]
)

fig.show()

# Plot filtered signal

N = 4 # filter order
Wn = 0.2 # (Hz) cutoff frequency

fig = go.Figure()

fig.add_trace(go.Scatter(x = df.index, y = df['y'], name = 'initial signal')) 

for timestep in ('2.5ms','50ms','100ms'):
    freq = 1000/float(timestep.replace('ms',''))
    df_res = df[['y']].resample(timestep).mean()
    print(df_res.head())
    b, a = butter(N, Wn, 'low',fs=freq)
    fig.add_trace(go.Scatter(x = df_res.index, y = filtfilt(b, a, df_res['y']), name = ' resampled '+str(freq)+' Hz')) 


fig.update_layout(
    title="Cutoff frequency 0.2 Hz - "+trip_1,
    xaxis_title="time (s)",
    yaxis_title="acceleration (m/s^2)",
    yaxis_range=[-3,3]
)
fig.show()
