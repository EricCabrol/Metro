import os 
import glob

# Problem specific variables

data_folder = './data/'
# records = glob.glob(data_folder+'L*')
records = [os.path.basename(x) for x in glob.glob(data_folder+'L*') if len(os.path.basename(x)) > 3]

print(records)