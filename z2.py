import os
import glob
import metro
from pathlib import Path

data_folder = "./data/"
data_path = Path(data_folder)
trip = 'L4_Montparnasse_-_Reaumur_-_soft-2024-03-29_08-07-51'

calib_choices = {"calibrated":True,"uncalibrated":False}
accel_files = {"calibrated":"Accelerometer.csv","uncalibrated":"AccelerometerUncalibrated.csv"}


for calib_key in calib_choices.keys():
    if calib_choices[calib_key] is True:
        record = metro.Record(data_path / trip / accel_files[calib_key])
        sampling_frequency = record.get_frequency()
        print('Identified sampling frequency = '+f"{sampling_frequency:.1f}"+' for trip'+trip)