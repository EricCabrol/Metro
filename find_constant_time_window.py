import pandas as pd
import plotly.graph_objects as go
from scipy.signal import filtfilt, butter

data_folder = './data/'
trip_1 = 'L4_Montparnasse_Reaumur_bag-2024-01-25_12-16-45'
fs_uncalibrated = 400 # acceleration sampling frequency
tol = 0.3 # tolerance to consider the signal constant (m/s^2)
min_stop_duration = 15 # minimum time window (s)

# Trying to segment the signal by identifying time windows when the accel is almost constant
# Process uncalibrated data, since calibrated accel is not constant when the metro is stopped ... 


# Filter parameters
N = 4
Wn = 2 # low-pass frequency
# b1, a1 = butter(N, Wn, 'low',fs=50) # Calibrated accel is sampled at 50 Hz
b2, a2 = butter(N, Wn, 'low',fs=fs_uncalibrated) # Uncalibrated accel is sampled at 400 Hz


df = pd.read_csv(data_folder+trip_1+'/AccelerometerUncalibrated.csv')
df['time'] = df['time']-df['time'][0] # Reset initial time
df['y_filt'] = filtfilt(b2, a2, df['y']) # Add a filtered column

tmp = 0 # accel init
begin = 0 # init
end = 0 # index init
df['stop'] = 0 # initialize a new column, boolean like (True if metro stopped) 

with open(data_folder+trip_1+"/timestamps.txt", mode="w") as output_file:
    output_file.write("Timestamps for trip "+trip_1+"\n")

    for ind in df.index:
        if abs(df['y_filt'][ind]-tmp) < tol: # changed y to y_filt
            end = ind
        else:
            # print(begin, end)
            if (end-begin) > fs_uncalibrated*min_stop_duration:
                df.loc[begin:end,'stop'] = 1 # TODO : check
                output_file.write(str(df['time'][begin]/1e9)+" stop\n")
                output_file.write(str(df['time'][end]/1e9)+" start\n")

            # reinitialize index and value at the beginning of the window
            begin = ind
            tmp = df['y_filt'][ind]

fig = go.Figure()

fig.add_trace(go.Scatter(x = df['time']/1e9, y = df['y'], name = 'uncalibrated')) 
fig.add_trace(go.Scatter(x = df['time']/1e9, y = filtfilt(b2, a2, df['y']), name = 'uncalibrated filtered')) 
fig.add_trace(go.Scatter(x = df['time']/1e9, y = df['stop'], name = 'stop')) 

fig.update_layout(
    title="Uncalibrated data",
    xaxis_title="time (s)",
    yaxis_title="acceleration (m/s^2)",
    yaxis_range=[-4,4]
)

fig.show()