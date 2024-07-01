import zipfile
import glob
import os
from pathlib import Path


# Unzip files found in zip directory, and move them in data

source_folder = './zip'
dest_folder = './data'

zip_files = glob.glob(source_folder+'/*.zip')

for file in zip_files:
    subdir = Path(file).stem  # returns filename without extension
    print(subdir)
    target = Path(dest_folder) / subdir
    if os.path.exists(target):
        print(subdir+' already exists')
    else:
        try:
            with zipfile.ZipFile(file, 'r') as zip_ref:
                zip_ref.extractall(os.path.join(dest_folder,subdir))
            os.remove(file)
        except:
            print("Could not unzip "+subdir)
