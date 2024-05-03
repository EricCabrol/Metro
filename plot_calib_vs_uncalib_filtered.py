import pandas as pd
import plotly.graph_objects as go
from scipy.signal import filtfilt, butter
from pathlib import Path
import scipy.fft as fft
import matplotlib.pyplot as plt
import numpy as np

data_folder = Path('./data')

trip_1 = 'L4_Montparnasse_-_Reaumur_bag-2024-01-25_12-16-45'
t_max = 999 # max time (s) 
fs_uncalibrated = 400 # Uncalibrated acceleration sampling frequency


# Filters definition
N = 4 # filter order
Wn = 0.5 # cutoff frequency
b1, a1 = butter(N, Wn, 'low',fs=50) # Calibrated accel is sampled at 50 Hz
b2, a2 = butter(N, Wn, 'low',fs=fs_uncalibrated) 

fig = go.Figure()

df = pd.read_csv(data_folder / trip_1 / 'AccelerometerUncalibrated.csv')
df['time'] = df['time']-df['time'][0]
df_sel = df[df['time']<t_max*1e9] # (optional) trimming to t_max seconds
df_sel['y_filt'] = filtfilt(b2, a2, df_sel['y']) # Add a filtered column

fig.add_trace(go.Scatter(x = df_sel['time']/1e9, y = df_sel['y'], name = 'uncalibrated')) 
fig.add_trace(go.Scatter(x = df_sel['time']/1e9, y = df_sel['y_filt'], name = 'uncalibrated filtered')) 

fig.update_layout(
    title="Comparison of raw vs filtered uncalibrated data - Low-pass "+\
            str(N)+"th order Butterworth filter - Cutoff frequency "+str(Wn)+" Hz",
    xaxis_title="time (s)",
    yaxis_title="acceleration (m/s^2)",
    yaxis_range=[-4,4]
)

df = pd.read_csv(data_folder / trip_1 / 'Accelerometer.csv')
df['time'] = df['time']-df['time'][0]
df_sel = df[df['time']<t_max*1e9]
fig.add_trace(go.Scatter(x = df_sel['time']/1e9, y = df_sel['y'], name = 'calibrated')) 
fig.add_trace(go.Scatter(x = df_sel['time']/1e9, y = filtfilt(b1, a1, df_sel['y']), name = 'calibrated filtered')) 

fig.update_layout(
    title="Comparison of raw vs filtered uncalibrated data - Low-pass "+str(N)+\
          "th order Butterworth filter - Cutoff frequency "+str(Wn)+" Hz",
    xaxis_title="time (s)",
    yaxis_title="acceleration (m/s^2)",
    yaxis_range=[-4,4]
)

fig.show()

# Adding Fourier transform

# Calculate the Fourier Transform
X = fft.fft(df_sel['y'].values)
freqs = fft.fftfreq(df_sel['y'].size, d=1/fs_uncalibrated)  # Calculate the frequencies

plt.plot(freqs, np.abs(X))
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.xlim([0, 10])  # Display frequencies from 0 to 10 Hz
plt.ylim([0, 10000])
plt.show()


X = fft.fft(df_sel['y_filt'].values)
freqs = fft.fftfreq(df_sel['y_filt'].size, d=1/fs_uncalibrated)  # Calculate the frequencies

plt.plot(freqs, np.abs(X))
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.xlim([0, 10])  # Display frequencies from 0 to 10 Hz
plt.ylim([0, 10000])
plt.show()