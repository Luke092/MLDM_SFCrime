# Preleva le prime n istanze e sostituisce l'attributo "Dates"
# con gli attributi "Season" e "Daily range"



from utilities import *

n = 100000
ds, intest = dsFromCSV('./Dataset/train.csv')
new_ds = []
intest = intest[1:]
intest.insert(0, 'Season')
intest.insert(1, 'Daily range')
seasons = {0: 'winter', 1: 'spring', 2: 'summer', 3: 'autumn'}
daily_ranges = {0: 'night', 1: 'morning', 2: 'afternoon', 3: 'evening'}
for i in range(0,n):
        date = ds[i]['Dates']
        splitted_date = date.split(' ')
        day,time = splitted_date[0].strip(), splitted_date[1].strip()
        month = day.split('-')
        month = int(month[1])
        hour = time.split(':')
        hour = int(hour[0])
        season = seasons[(month-1)/3]
        daily_range = daily_ranges[hour/6]
        ds[i]['Season'] = season
        ds[i]['Daily range'] = daily_range
        del(ds[i]['Dates'])
        new_ds.append(ds[i])
dsToCSV('./Dataset/train_new.csv',new_ds,intest)
