from utilities import *
import time
import re

def removeAtts(ds, intest, atts):
    if not atts:
        return ds, intest
    for att in atts:
        intest.remove(att)
    for i in range(len(ds)):
        for att in atts:
            del ds[i][att]
    return ds, intest

# Global variables
limit_X_min = -122.519703 #-122.511076
limit_X_max = -122.268906 #-122.365671
limit_Y_min = 37.684092 #37.707777
limit_Y_max = 37.871601 #37.836333

def processSDR(ds, intest):
    n = len(ds)
    new_ds = []
    intest.remove('Dates')
    intest.insert(0, 'Season')
    intest.insert(1, 'DailyRange')
    seasons = {0: 'winter', 1: 'spring', 2: 'summer', 3: 'autumn'}
    daily_ranges = {0: 'night', 1: 'morning', 2: 'afternoon', 3: 'evening'}
    for i in range(n):
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

def processGrid(ds, gridSide):
    ds_new = []

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
        if limit_X_min <= x <= limit_X_max:
            if x < min_x:
                min_x = x
            if x > max_x:
                max_x = x

        if limit_Y_min <= y <= limit_Y_max:
            if y < min_y:
                min_y = y
            if y > max_y:
                max_y = y

        ds_new.append(ds[i])
        printProgress(i,n)

    step_x = (max_x - min_x)/gridSide
    step_y = (max_y - min_y)/gridSide

    for row in ds_new:
        row['X'] = int((float(row['X']) - min_x)/step_x)
        row['Y'] = int((float(row['Y']) - min_y)/step_y)
    return ds_new

def processCross(ds, intest):
    n = len(ds)
    intest.remove('Address')
    intest.insert(4, 'isCross')
    new_ds = []
    for i in range(n):
        address = ds[i]['Address']
        isCross = re.search(' / ', address) is not None
        del ds[i]['Address']
        ds[i]['isCross'] = isCross
        new_ds.append(ds[i])
        printProgress(i,n)
    return new_ds, intest

def address_to_type(ds):
    if (ds[0]['Address'] == None):
        return None

    crosses = []

    for row in ds:
        cross = row['Address'].split("/")
        if (len(cross) == 1):
            t = row['Address'].strip()[-2:]
            row['Address'] = t
        elif(cross[0].strip()[-2:] == cross[1].strip()[-2:]):
            row['Address'] = cross[0].strip()[-2:]
        else:
            t1 = cross[0].strip()[-2:]
            t2 = cross[1].strip()[-2:]
            if(t1 + "/" + t2 in crosses):
                row['Address'] = t1 + "/" + t2
            elif (t2 + "/" + t1 in crosses):
                row['Address'] = t2 + "/" + t1
            else:
                row['Address'] = t1 + "/" + t2
                crosses.append(row['Address'])

    return ds

def processStreet(ds, intest):
    n = len(ds)
    intest.remove('Address')
    intest.insert(4, 'StreetType')
    new_ds = []
    crosses = []
    for i in range(n):
        address = ds[i]['Address']
        isCross = re.search(' / ', address) is not None
        if not isCross:
            streetType = address[-2:]
        else:
            streetTypes = re.split(' / ', address)
            streetTypes = [s[-2:] for s in streetTypes]
            streetType = ' / '.join(streetTypes)
            streetTypeReversed = ' / '.join(reversed(streetTypes))
            if not streetType in crosses and not streetTypeReversed in crosses:
                crosses.append(streetType)
            if streetTypeReversed in crosses:
                streetType = streetTypeReversed
        del ds[i]['Address']
        ds[i]['StreetType'] = streetType
        new_ds.append(ds[i])
        printProgress(i,n)
    return new_ds, intest

def getCorrectCoordinates(ds):

	n = len(ds)

	for i in range(n):
		x = float(ds[i]['X'])
		y = float(ds[i]['Y'])
		x_ok = False
		y_ok = False
		if (limit_X_min <= x <= limit_X_max):
			x_ok = True

		if (limit_Y_min <= y <= limit_Y_max):
			y_ok = True

		if not(x_ok) or not(y_ok):
			if ds[i]['Address'] == 'FLORIDA ST / ALAMEDA ST':
				ds[i]['Address'] = 'TREAT ST'
			if ds[i]['Address'] == 'ARGUELLO BL / NORTHRIDGE DR':
				ds[i]['Address'] = 'ARGUELLO BL'
			ds[i]['X'], ds[i]['Y'] = get_coordinates(ds[i]['Address'] + ', SAN FRANCISCO')
			ds[i]['X'], ds[i]['Y'] = str(ds[i]['X']), str(ds[i]['Y'])
			time.sleep(0.2)
		printProgress(i,n)

	return ds
