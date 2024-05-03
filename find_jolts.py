# Objective : find the "jolts" of positive acceleration at the very end of the braking phase
# Since the amplitude of these peaks seems higher on the calibrated acceleration, 
# we'll use it instead of the uncalibrated one
# 
# (script used for the ep.3 of the LinkedIn series)

import pandas as pd
import plotly.graph_objects as go
from scipy.signal import filtfilt, butter
from pathlib import Path

data_folder = Path('./data')

trip_1 = 'L4_Montparnasse_-_Reaumur_bag-2024-01-25_12-16-45'

fs_calibrated = 50 # sampling frequency
min_amplitude_jolt = 1.5 # minimum acceleration to consider the peak as a jolt (m/s^2)
min_amplitude_restart = 0.5 # minimum acceleration to consider that the metro restarts (m/s^2)
min_stop_duration = 20 # min duration before peak and restart (s)


df = pd.read_csv(data_folder / trip_1 / 'Accelerometer.csv')
df['time'] = df['time']-df['time'][0] # Reset initial time

begin = 0 # init
end = 0 # index init
df['stop'] = 0 # initialize a new column, boolean like (True if metro stopped)
stopped = False

with open(data_folder / trip_1 / "timestamps.txt", mode="w") as output_file:
    output_file.write("Timestamps for trip "+trip_1+"\n")

    for ind in df.index:
        accel = df['y'][ind]
        if (accel > min_amplitude_jolt) :
            begin = ind
            stopped = True
        if stopped and (accel > min_amplitude_restart) and (ind-begin) > fs_calibrated*min_stop_duration:
            stopped = False
            end = ind
            df.loc[begin:end,'stop'] = 1
            output_file.write(str(df['time'][begin]/1e9)+" stop\n")
            output_file.write(str(df['time'][end]/1e9)+" start\n")


fig = go.Figure()

fig.add_trace(go.Scatter(x = df['time']/1e9, y = df['y'], name = 'acceleration')) 
fig.add_trace(go.Scatter(x = df['time']/1e9, y = df['stop'], name = 'stop')) 

fig.update_layout(
    title="Calibrated acceleration and stops for trip "+trip_1,
    xaxis_title="time (s)",
    yaxis_title="acceleration (m/s^2)",
    yaxis_range=[-4,4]
)

fig.show()