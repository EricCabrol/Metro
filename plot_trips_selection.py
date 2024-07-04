import pandas as pd
import plotly.graph_objects as go
from scipy.signal import filtfilt, butter
from pathlib import Path
import metro
import glob
import re
import os 



# Problem specific variables

data_folder = "./data/"
data_path = Path(data_folder) # used later in the script
# if len > 4 condtion added to exclude "non-trip" folders such as L4 or L13 that contain individual sections of each line
records = [os.path.basename(x) for x in glob.glob(data_folder+'L*') if len(os.path.basename(x)) > 4]
# print(records)

# SHOW AVAILABLE RECORDINGS


def get_date(name):
    try:
        date_match = re.search('\d{4}-\d{2}-\d{2}',name)
        return(date_match.group(0))
    except:
        print("Couldn't parse date in folder "+name)
        return('1900-01-01')


def reformat_record(folder,name): # used only for readability of the output
    # trip_name = name[len(folder)+1:] # remove source folder from full name
    tripObj = metro.Trip(name) 
    try:
        trip_date = (re.search('\d{4}-\d{2}-\d{2}',name)).group(0)
    except:
        trip_date = '1900-01-01'

    return (trip_date, tripObj.get_line(), tripObj.get_start(), tripObj.get_end())

for counter, record in enumerate(sorted(records,key=get_date, reverse=True)): #  reverse chronological order
    print (counter, '\t', *reformat_record(data_folder,record)) # unpacking the list with the * operator



# LET THE USER SELECT THE TRIPS HE WANTS TO PLOT

def get_ids_from_input():
    selection = input("Enter selection:(ex : 1,3-5)\n")
    fields = selection.split(',')
    ids = []
    for field in fields:
        if re.search('-',field):
            tmp = field.split('-')
            ids.extend(range(int(tmp[0]),int(tmp[1])+1))
        else:
            ids.append(field)
    return(ids)


ids = get_ids_from_input()
trips = [sorted(records,key=get_date, reverse=True)[int(i)] for i in ids] # TODO : fix error ... or revert

# trips = ('L4_Etienne_Marcel_-_Montparnasse_-_brutal_2_stops_annotated-2024-06-24_17-22-44','dummy')

# Do we plot calibrated, uncalibrated, filtered or unfiltered data ? 

calib_choices = {"calibrated":True,"uncalibrated":False}
filter_choices = {"filtered":False,"unfiltered":True}

t_max = 900 # (s) can be used to truncate the trips (to reduce processing time)

# Parameters below shouldn't change for a given smartphone / SensorLogger configuration

accel_files = {"calibrated":"Accelerometer.csv","uncalibrated":"AccelerometerUncalibrated.csv"}

# Filter parameters
N = 4 # filter order
Wn = 2 # (Hz) cutoff frequency

fig = go.Figure()

for trip in trips:
    print('Processing trip '+trip)

    for calib_key in calib_choices.keys(): 
        if calib_choices[calib_key] is True:
            try:
                df = pd.read_csv(data_path / trip / accel_files[calib_key])
            except:
                print(accel_files[calib_key]+" not found for trip "+trip)
                continue
            try: # Extract sampling frequency from the record
                record = metro.Record(data_path / trip / accel_files[calib_key])
                sampling_frequency = record.get_frequency()
                print('Identified sampling frequency = '+f"{sampling_frequency:.1f} Hz"+' for trip '+trip)
            except:
                print('could not identify sampling frequency for trip '+trip)
            
            df['time'] = df['time']-df['time'][0] # Here we choose to reset t0 to 0
            df = df[df['time'] < t_max*1e9] # Truncate to t_max and convert to ns
            # Plotting filtered and/or unfiltered 
            if filter_choices['unfiltered'] is True:
                fig.add_trace(go.Scatter(x = df['time']/1e9, y = df['y'], name = trip+' '+calib_key))
            if filter_choices['filtered'] is True:
                b, a = butter(N, Wn, 'low',fs=sampling_frequency) # using identified sampling frequency
                fig.add_trace(go.Scatter(x = df['time']/1e9, y = filtfilt(b, a, df['y']), name = trip+' '+calib_key+' filt. '+str(Wn)+' Hz')) 

fig.update_layout(
    title = '  VS  '.join([x for x in trips]),
    xaxis_title = "time (s)",
    yaxis_title = "acceleration (m/s^2)",
    yaxis_range=[-4,4]
)

fig.show()
