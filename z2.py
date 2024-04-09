import os
import re
import unidecode
from pathlib import Path
# print(Path.cwd())
# for filepath in Path.cwd().glob('*.py'):
#     print(filepath)
#     print(filepath.name)



folder = './data'
subfolders = [ f.name for f in os.scandir(folder) if f.is_dir() ]
# print(subfolders)

# trip = r'L4_Cité_-_Montparnasse_-_avg-2024-03-27_20-04-20'
# trip = r'L4_-_Cité_-_Montparnasse_-_avg-2024-03-27_20-04-20'
# trip = r'L4_-_Les_Halles_-_Montparnasse_-_avg-2024-03-27_20-04-20'
# trip = r'L6_Raspail_-_Montparnasse_-_side-2024-03-04_21-01-22'
trip = r'L3_St-Lazare_-_Sentier-2024-01-24_08-05-03'

start = re.search('^L\d+[-_]*([\w_]+)_-_',unidecode.unidecode(trip))
if start is not None:
    print(re.search('^L\d+[-_]*([\w_]+)_-_',unidecode.unidecode(trip)).group(0))
else:
    print("start not found")
    
# try:
#     start = re.search('^L\d+[-_]*([\w_]+)_-_',unidecode.unidecode(trip))
#     print(start)
#     # print(re.search('^L\d+[-_]*([\w_]+)_-_',unidecode.unidecode(trip)).group(0))
# except:
#     print("failed")
#     pass

