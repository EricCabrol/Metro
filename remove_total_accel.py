import glob
import os

source_folder = './data'

files = glob.glob(source_folder+'/**/TotalAcceleration.csv')

for file in files:
    print(file)
    os.remove(file)