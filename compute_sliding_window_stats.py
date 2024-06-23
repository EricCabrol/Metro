import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import metro 



def compute_sliding_window_stats(df, column_name, window_size):

    # Extract the timeseries data
    timeseries = df[column_name].values

    # Initialize lists to store the results
    means = []
    variances = []

    # Compute mean and variance in the sliding window
    for i in range(len(timeseries) - window_size + 1):
        window = timeseries[i:i + window_size]
        means.append(np.mean(window))
        variances.append(np.var(window))

    return means, variances

def identify_time_windows(signal, threshold, min_window_length):

    
    below_threshold = signal < threshold
    below_threshold = below_threshold.astype(int)
    
    # Identify the start and end of each window
    diff = np.diff(below_threshold, prepend=0, append=0)
    starts = np.where(diff == 1)[0]
    ends = np.where(diff == -1)[0]
    
    # Filter out windows that are shorter than the minimum length
    valid_windows = [(start, end-1) for start, end in zip(starts, ends) if (end - start) >= min_window_length]

    result_vector = np.zeros_like(signal, dtype=int)
    for start, end in valid_windows:
        result_vector[start:end+1] = 1

    return valid_windows, result_vector

# Application
csv_file = 'data/L4_Montparnasse_-_Reaumur_-_bag-2024-01-25_12-16-45/AccelerometerUncalibrated.csv'
column_name = 'y'
record = metro.Record(csv_file)
sampling_frequency = record.get_frequency()
print("Sampling frequency = ",sampling_frequency)
window_size = int(2 * sampling_frequency)
min_stopped_time = int(10 * sampling_frequency)
df = pd.read_csv(csv_file)

means, variances = compute_sliding_window_stats(df, column_name, window_size)

windows, stopped = identify_time_windows(np.array(variances), 0.01, min_stopped_time)



# Plot the time evolution of the variance
plt.figure(figsize=(10, 6))
# plt.plot(range(len(variances)), variances, label='Variance')
plt.plot(range(len(variances)), stopped, label='Stopped')
plt.plot(df.index, df[column_name], label='Accel')
plt.xlabel('Time')
plt.ylabel('Variance')
plt.title('Time Evolution of the Variance')
plt.legend()
plt.show()