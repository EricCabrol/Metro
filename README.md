# Post-processing of Sensor Logger recordings for metro braking data analysis

## Main scripts

**Plotting data**

- `plot_all_decel.py` : plots all calibrated accelerations found in a folder

- `plot_trips_selection.py` allows to compare a selection of trips, both for calibrated/uncalibrated and raw/filtered data

- `plot_FFT_single_trip.py`: plots the FFT of calibrated accel of a single trip


**Identifying stops from acceleration recordings**

- `find_constant_time_window.py` was the first attempt to identify time windows where accel is constant. Leads to false positives
(see ep.2 : https://www.linkedin.com/pulse/data-analysis-paris-metro-ep2-eric-cabrol-tq7ye/)

- `find_jolts.py` : second attempt, using "jolt-back" peaks => seems better
(see ep.3 : https://www.linkedin.com/pulse/data-analysis-paris-metro-ep3-eric-cabrol-lynie)
A file `timestamps.txt` is generated in each folder. It still requires a manual validation, then the file must be saved as `timestamps_validated.txt`. Note that the calibrated acceleration could be useful, because it reaches consistently 3m/s peaks that could be useful to identify the stops. 

- `find_jolts_all.py` : WIP to detect jolts in all recordings of a given directory

**Identifying stops from recordings names**

- `find_stops_from_trip_name.py` : test with difflib SequenceMatcher.To be reincorporated in `metro.py` module

**Module**

- `metro.py` : contains a class Trip to retrieve all useful information from the trip name. Shall I also manage quantitative data with this class ? 


## Utilities


NB : zip files exported from SensorLogger must be manually downloaded from Google Drive into `zip` folder

1. `unzip_recordings.py` allows to unzip recordings in `data` 
2. `remove_total_accel.py` removes `TotalAcceleration.csv` files, because they contain the same data as `AccelerometerUncalibrated.csv`
