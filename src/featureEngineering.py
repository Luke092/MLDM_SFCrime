from utilities import *
import time

def processSDR(ds, intest):
    n = len(ds)
    new_ds = []
    intest.remove('Dates')
    intest.insert(0, 'Season')
    intest.insert(1, 'DailyRange')
    seasons = {0: 'winter', 1: 'spring', 2: 'summer', 3: 'autumn'}
    daily_ranges = {0: 'night', 1: 'morning', 2: 'afternoon', 3: 'evening'}
    for i in range(0,len(ds)):
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
        ds[i]['DailyRange'] = daily_range
        del(ds[i]['Dates'])
        new_ds.append(ds[i])
        printProgress(i,n)
    return new_ds, intest

def processGrid(ds, intest, gridSide):
    ds_new = []

    limit_X_min = -122.519703 #-122.511076
    limit_X_max = -122.268906 #-122.365671
    limit_Y_min = 37.684092 #37.707777
    limit_Y_max = 37.871601 #37.836333

    min_x = float(ds[0]['X'])
    max_x = float(ds[0]['X'])
    min_y = float(ds[0]['Y'])
    max_y = float(ds[0]['Y'])

    n = len(ds)

    for i in range(n):
        x = float(ds[i]['X'])
        y = float(ds[i]['Y'])
        x_ok = False
        y_ok = False
        if (limit_X_min <= x <= limit_X_max):
            if x < min_x:
                min_x = x
            if x > max_x:
                max_x = x
            x_ok = True
            
        if (limit_Y_min <= y <= limit_Y_max):
            if y < min_y:
                min_y = y
            if y > max_y:
                max_y = y
            y_ok = True

        if not(x_ok) or not(y_ok):
            if ds[i]['Address'] == 'FLORIDA ST / ALAMEDA ST':
                ds[i]['Address'] = 'TREAT ST'
            if ds[i]['Address'] == 'ARGUELLO BL / NORTHRIDGE DR':
                ds[i]['Address'] = 'ARGUELLO BL'
            ds[i]['X'], ds[i]['Y'] = get_coordinates(ds[i]['Address'] + ', SAN FRANCISCO')
            ds[i]['X'], ds[i]['Y'] = str(ds[i]['X']), str(ds[i]['Y'])
            time.sleep(0.2)
##            print str(i), ds[i]['X'], ds[i]['Y']
##             ds[i]['X'], ds[i]['Y'] = (limit_X_min + limit_X_max)/2.0, (limit_Y_min + limit_Y_max)/2.0
            
        ds_new.append(ds[i])
        printProgress(i,n)

    step_x = (max_x - min_x)/gridSide
    step_y = (max_y - min_y)/gridSide

    for row in ds_new:
        row['X'] = str(int((float(row['X']) - min_x)/step_x))
        row['Y'] = str(int((float(row['Y']) - min_y)/step_y))
    return ds_new
