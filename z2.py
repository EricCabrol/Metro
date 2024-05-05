import os
from pathlib import Path

data_folder = Path('./data_test')
subfolders = [ f.path for f in os.scandir(data_folder) if f.is_dir() ]
for trip in subfolders:
    print(Path(trip).stem)