import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
import re
from scipy.signal import filtfilt, butter

"""
Comparison of the same trip recorded with my Pixel 4 and a Samsung A33 
(06/2024)
Notes : 
- the sampling frequency of each one is different, and hard-coded in the script
- SensorLogger was used on the Pixel, while Physics Toolbox is used on the A33
- timestamps obtained with Physics Toolbox are not always consistent, but this doesn't seem to impact the results
- cleanup is done on the file generated with Physics Toolbox, because of its weird formatting
- since both use uncalibrated data, an offset is added to compensate for the calibration difference
- the g-force was recorded (by mistake) instead of the linear acceleration with the A33, so the curve amplitude is multiplied by 9.81
- a 0.2 Hz cutoff frequency is used for the Butterworth filter

See https://www.linkedin.com/pulse/data-analysis-paris-metro-ep6-eric-cabrol-cj4re 

"""


data_folder = Path('comparo')
filename = '2024-06-1708.56.55 a33 comparo slow.csv'

df = pd.read_csv(data_folder / filename,sep=';',decimal=',')
record_date = re.match('\d{4}-\d{2}-\d{2}',filename).group(0) # extract the date from the filename
df['dayAndtime'] = record_date + ' ' + df['time'].astype(str) # add the date to get a proper datetime field
df['DateTime'] = pd.to_datetime(df['dayAndtime'], format='%Y-%m-%d %H:%M:%S:%f')
df = df.set_index('DateTime')


# df2 = pd.read_csv(data_folder / 'Comparo_slow-2024-06-17_06-57-00' / 'Accelerometer.csv')
df2 = pd.read_csv(data_folder / 'Comparo_slow-2024-06-17_06-57-00' / 'AccelerometerUncalibrated.csv')
df2['DateTime'] = pd.DatetimeIndex(df2['time']) + pd.offsets.DateOffset(hours=2)
df2 = df2.set_index('DateTime')

offset_correction = 0.25
gravity = 9.81 

# PLOT NON-FILTERED DATA

fig = go.Figure()
fig.add_trace(go.Scatter(x = df.index, y = df['gFy'] * gravity + offset_correction, name = 'A33'))
fig.add_trace(go.Scatter(x = df2.index, y = df2['y'], name = 'Pixel 4 XL'))


fig.update_layout(
    title="A33 Physics Toolbox vs Pixel 4 SensorLogger",
    xaxis_title="time (s)",
    yaxis_title="acceleration (m/s^2)",
    yaxis_range=[-2,3.5]
)
fig.show()

# PLOT FILTERED DATA

# Filter parameters
N = 4 # filter order
Wn = 0.2 # (Hz) cutoff frequency
b1, a1 = butter(N, Wn, 'low',fs=500)
b2, a2 = butter(N, Wn, 'low',fs=20)


fig = go.Figure()
fig.add_trace(go.Scatter(x = df.index, y = filtfilt(b1, a1, df['gFy'])*gravity + offset_correction, name = 'A33'))
fig.add_trace(go.Scatter(x = df2.index, y = filtfilt(b2, a2, df2['y']), name = 'Pixel 4 XL'))


fig.update_layout(
    title="A33 Physics Toolbox vs Pixel 4 SensorLogger - filtered 0.2 Hz",
    xaxis_title="time (s)",
    yaxis_title="acceleration (m/s^2)",
    yaxis_range=[-2,2]
)
fig.show()