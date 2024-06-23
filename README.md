# Post-processing of Sensor Logger recordings for metro braking data analysis

Some trains of Paris metro line 4 brake really hard, which sometimes can almost become dangerous for the passengers if they don't hang on.
I wanted to check if i could identify which level of deceleration gets perceived as "too harsh", so I decided to record the trips using an Android app called SensorLogger, and do some signal processing, playing with Python, Pandas, SciPy ... 

More comments can be found on the LinkedIn posts I wrote : 
- [episode 01 : recording trips](https://www.linkedin.com/pulse/data-analysis-paris-metro-ep1-eric-cabrol-01kie)
- [episode 02 : filtering signals](https://www.linkedin.com/pulse/data-analysis-paris-metro-ep2-eric-cabrol-tq7ye/)
- [episode 03 : identifying stops](https://www.linkedin.com/pulse/data-analysis-paris-metro-ep3-eric-cabrol-lynie)
- [episode 04 : organizing data](https://www.linkedin.com/pulse/data-analysis-paris-metro-ep4-eric-cabrol-ar0ye)
- [episode 05 : finding the right cutoff frequency](https://www.linkedin.com/pulse/data-analysis-paris-metro-ep5-eric-cabrol-grnte/)
- [episode 06 : comparing phones](https://www.linkedin.com/pulse/data-analysis-paris-metro-ep6-eric-cabrol-cj4re/) 



## Main scripts

### Plotting data

- `plot_all_decel.py` : plots all calibrated accelerations found in a folder

- `plot_trips_selection.py` allows to compare a selection of trips, both for calibrated/uncalibrated and raw/filtered data

- `plot_FFT_single_trip.py`: plots the FFT of calibrated accel of a single trip


### Identifying stops from acceleration recordings

- `find_constant_accel.py` was the first attempt to identify time windows where accel is constant. Leads to false positives
(see ep.2 : https://www.linkedin.com/pulse/data-analysis-paris-metro-ep2-eric-cabrol-tq7ye/)

- `find_jolts.py` : second attempt, using "jolt-back" peaks => seems better
(see ep.3 : https://www.linkedin.com/pulse/data-analysis-paris-metro-ep3-eric-cabrol-lynie)
A file `timestamps.txt` is generated in each folder. It still requires a manual validation, then the file must be saved as `timestamps_valid.txt`.

- `find_jolts_all.py` : detect jolts in all recordings of a given directory
=> in fact there are as many difficulties to identify the stops, so I switched back to the constant accel solution

- `find_constant_accel_all.py` : asks for confirmation after each trip, which allows to modify the timestamps file before validating
30th May 2024 : still often fails with "Could not find annotations" even when the number of stops seems OK #TODO

### Identifying stops from recordings names

- previously done in `find_stops_from_trip_name.py`, now in `metro.py` module  

### Cut trips (once stops are validated)

- `check_timestamps.py` : only checks that there are as many stops in the timestamps file as there should be from the trip name

- `cut_trips.py` : cuts the trip into sections. Could be merged with `check_timestamps.py` #TODO 



## Module

- `metro.py` : contains a class named Trip to retrieve all useful information from the trip name. Shall I also manage quantitative data with this class (eg sampling frequency) ? 


## Utilities

- `study_resampling.py` checks the influence of the initial sampling frequency on the filtered results

NB : zip files exported from SensorLogger must be manually downloaded from Google Drive into `zip` folder

1. `unzip_recordings.py` allows to unzip recordings in `data` 
2. `remove_total_accel.py` removes `TotalAcceleration.csv` files, because they contain the same data as `AccelerometerUncalibrated.csv`
