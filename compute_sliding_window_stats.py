import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt




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

# Example usage
csv_file = 'data/L4_Montparnasse_-_Reaumur_-_bag-2024-01-25_12-16-45/Accelerometer.csv'
column_name = 'y'
window_size = 100
df = pd.read_csv(csv_file)

means, variances = compute_sliding_window_stats(df, column_name, window_size)

# Print the results
# print("Means:", means)
# print("Variances:", variances)



# Plot the time evolution of the variance
plt.figure(figsize=(10, 6))
plt.plot(range(len(variances)), variances, label='Variance')
plt.plot(df.index, df[column_name], label='Accel')
plt.xlabel('Time')
plt.ylabel('Variance')
plt.title('Time Evolution of the Variance')
plt.legend()
plt.show()