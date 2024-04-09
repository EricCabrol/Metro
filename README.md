# Post-processing of Sensor Logger data for metro recordings



1. Zip files are downloaded from Google Drive into `zip` folder
2. `unzip_recordings.py` allows to unzip recordings in `data` 
3. `remove_total_accel.py` removes all `TotalAcceleration.csv`, because they contain the same data as `AccelerometerUncalibrated.csv`
3. `plot_two_trips.py` allows to compare two recordings, both for calibrated and uncalibrated data
4. `find_constant_time_window.py` to process one trip and identify time windows where accel is constant
5. A file `timestamps.txt` is generated in each folder. It still requires a manual validation, then the file must be saved as `timestamps_validated.txt`. Note that the calibrated acceleration could be useful, because it reaches consistently 3m/s peaks that could be useful to identify the stops. 
6. `find_stops.py` : ongoing work
