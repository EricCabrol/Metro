import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt


data_folder = Path('./data')

trip_1 = 'L4_Montparnasse_-_Reaumur_-_bag-2024-01-25_12-16-45'

# df = pd.read_csv(data_folder / trip_1 / 'AccelerometerUncalibrated.csv', parse_dates=['time'],index_col='time')
df = pd.read_csv(data_folder / trip_1 / 'AccelerometerUncalibrated.csv')
# sampling_rate = 1 / np.diff(df['seconds_elapsed'])
# plt.hist(sampling_rate)
# plt.show()

# df['time'] = df['time']-df['time'][0] # Reset initial time
# print(df.head())
# print(1/(df['seconds_elapsed'][1]-df['seconds_elapsed'][0]))
# print(df.info())

df['DateTime'] = pd.DatetimeIndex(df['time'])
df = df.set_index('DateTime')
print(df.head())

df_res = df.resample('2.5ms').mean()
print(df_res.head())
# df_res = df_res.dropna()

sampling_rate = 1 / np.diff(df_res['seconds_elapsed'])
plt.hist(sampling_rate)
plt.show()