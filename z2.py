fs = {"calibrated" : 50, "uncalibrated" : 400 }
print(fs.keys())

trips = ('L4_Montparnasse_-_Reaumur_-_soft-2024-03-29_08-07-51',
         'L4_Montparnasse_-_Reaumur_bag-2024-01-25_12-16-45')

print('  VS  '.join([x for x in trips]))