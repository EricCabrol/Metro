import pandas as pd
from scipy.signal import filtfilt, butter
from pathlib import Path
import scipy.fft as fft
import matplotlib.pyplot as plt
import numpy as np

# PLOT FFT OF CALIBRATED ACCELERATION FOR A SINGLE TRIP


data_folder = Path("./data")
accel_file = "Accelerometer.csv"

trip_1 = "L4_Montparnasse_-_Reaumur_-_soft-2024-03-29_08-07-51"
t_max = 999 # max time (s) 
fs_calib = 50 # (Hz) sampling frequency

# Filter definition
N = 4 # filter order
Wn = 0.5 # cutoff frequency
b, a = butter(N, Wn, 'low',fs=fs_calib) # Calibrated accel is sampled at 50 Hz

df = pd.read_csv(data_folder / trip_1 / accel_file)
df['time'] = df['time']-df['time'][0]
df = df[df['time']<t_max*1e9] # (optional) trimming to t_max seconds
df['y_filt'] = filtfilt(b, a, df['y']) # Add a filtered column


# Calculate the Fourier Transform
X = fft.fft(df['y_filt'].values)
freqs = fft.fftfreq(df['y_filt'].size, d=1/fs_calib)  # Calculate the frequencies

plt.plot(freqs, np.abs(X))
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.xlim([0, 10])  # Display frequencies from 0 to 10 Hz
plt.ylim([0, 1000])
plt.show()
