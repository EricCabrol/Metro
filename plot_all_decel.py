import pandas as pd
import plotly.graph_objects as go
import os
from pathlib import Path


# Parse all directories in data folder

data_folder = Path('./data')
# data_folder = Path('./data_test')
subfolders = [ f.path for f in os.scandir(data_folder) if f.is_dir() ]


fig = go.Figure()

# plot accel on the Y axis
for sub in subfolders:
    try:
        df = pd.read_csv(Path(sub) / 'Accelerometer.csv') # rebuild Path object is required  (because sub isn't one)
        df['time'] = df['time']-df['time'][0] # Reset initial time of the recording to 0
        fig.add_trace(go.Scatter(x = df['time'], y = df['y'], name = sub))
    except:
        print("No Accelerometer.csv found in "+sub)

fig.update_layout(yaxis_range=[-4,4])
fig.show()