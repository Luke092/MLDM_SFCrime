from utilities import *
from sklearn.cluster import KMeans
from sklearn import preprocessing

import pandas as pd
import time
import re
import os


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
limit_X_min = -122.519703  # -122.511076
limit_X_max = -122.268906  # -122.365671
limit_Y_min = 37.684092  # 37.707777
limit_Y_max = 37.871601  # 37.836333


def processSDR(ds, intest):
    n = len(ds)
    new_ds = []
    # intest.remove('Dates')
    intest.insert(0, 'Season')
    intest.insert(1, 'DailyRange')
    seasons = {0: 'winter', 1: 'spring', 2: 'summer', 3: 'autumn'}
    daily_ranges = {0: 'night', 1: 'morning', 2: 'afternoon', 3: 'evening'}
    for i in range(n):
        date = ds[i]['Dates']
        splitted_date = date.split(' ')
        day, time = splitted_date[0].strip(), splitted_date[1].strip()
        month = day.split('-')
        month = int(month[1])
        hour = time.split(':')
        hour = int(hour[0])
        season = seasons[(month - 1) / 3]
        daily_range = daily_ranges[hour / 6]
        ds[i]['Season'] = season
        ds[i]['DailyRange'] = daily_range
        # del (ds[i]['Dates'])
        new_ds.append(ds[i])
        printProgress(i, n)
    return new_ds, intest


def processGrid(ds, gridSide):
    min_x, max_x, min_y, max_y = getMinMax()

    step_x = (max_x - min_x) / gridSide
    step_y = (max_y - min_y) / gridSide

    for row in ds:
        row['X'] = int((float(row['X']) - min_x) / step_x)
        row['Y'] = int((float(row['Y']) - min_y) / step_y)
    return ds


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
        printProgress(i, n)
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
        elif (cross[0].strip()[-2:] == cross[1].strip()[-2:]):
            row['Address'] = cross[0].strip()[-2:]
        else:
            t1 = cross[0].strip()[-2:]
            t2 = cross[1].strip()[-2:]
            if (t1 + "/" + t2 in crosses):
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
        printProgress(i, n)
    return new_ds, intest


def processDay(ds, intest):
    n = len(ds)
    intest.remove('DayOfWeek')
    intest.insert(3, 'Weekend')
    for i in range(n):
        day = ds[i]['DayOfWeek']
        if day == 'Saturday' or day == 'Sunday':
            ds[i]['Weekend'] = True
        else:
            ds[i]['Weekend'] = False
        del ds[i]['DayOfWeek']
        printProgress(i, n)
    return ds, intest

def processDate(ds, intest, toProcess='YMDH'):
    if not toProcess:
        return ds, intest
    n = len(ds)
    processable = {'Y':'Year', 'M': 'Month', 'D': 'DayOfMonth', 'H': 'Hour'}
    # intest.remove('Dates')
    ex = []
    pos = 0
    for key, value in processable.iteritems():
        if key in toProcess:
            intest.insert(pos,value)
            ex.append(value)
            pos += 1
    for i in range(n):
        date = ds[i]['Dates']
        splitted_date = date.split(' ')
        day, time = splitted_date[0].strip(), splitted_date[1].strip()
        day = day.split('-')
        time = time.split(':')
        processed = {'Y': day[0], 'M': day[1], 'D': day[2], 'H': time[0]}
        for key, value in processable.iteritems():
            if key in toProcess:
                ds[i][value] = int(processed[key])
        # del (ds[i]['Dates'])
        printProgress(i, n)
    return ds, intest, ex

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

        if not (x_ok) or not (y_ok):
            if ds[i]['Address'] == 'FLORIDA ST / ALAMEDA ST':
                ds[i]['Address'] = 'TREAT ST'
            if ds[i]['Address'] == 'ARGUELLO BL / NORTHRIDGE DR':
                ds[i]['Address'] = 'ARGUELLO BL'
            ds[i]['X'], ds[i]['Y'] = get_coordinates(ds[i]['Address'] + ', SAN FRANCISCO')
            ds[i]['X'], ds[i]['Y'] = str(ds[i]['X']), str(ds[i]['Y'])
            time.sleep(0.2)
        printProgress(i, n)

    return ds

def coordinate_normalization(save_on_file = False):
    print '\nCoordinate normalization'
    sets = ['train','test']
    result = []
    for dset in sets:
        df = pd.read_csv('./Dataset/' + dset + '.csv')
        min_max_scaler = preprocessing.MinMaxScaler()
        X_norm = min_max_scaler.fit_transform(df.X)
        Y_norm = min_max_scaler.fit_transform(df.Y)
        df_norm = pd.DataFrame({'X' : X_norm, 'Y' : Y_norm})
        result.append(df_norm)
        if save_on_file:
            print 'Saving on file'+'./Dataset/'+dset+'_XYnorm.csv'
            df_norm.to_csv(path_or_buf='./Dataset/' + dset + '_XYnorm.csv', sep=',', na_rep='', float_format=None, columns=None, header=True, index=False, index_label=None, mode='w', encoding=None, compression=None, quoting=None, quotechar='"', line_terminator='\n', chunksize=None, tupleize_cols=False, date_format=None, doublequote=True, escapechar=None, decimal='.')
    print 'Done'
    return result

def coordinate_quantization(side):
    sets = ['train','test']
    normalized = coordinate_normalization()
    index = 0
    print '\nCoordinate quantization'
    for dset in sets:
        df_X, df_Y = pd.DataFrame({'X': normalized[index].X}), pd.DataFrame({'Y': normalized[index].Y})
        print 'creating ','./Dataset/' + dset + '_XYquant_' + str(side) + '.csv'
        X_quant = KMeans(n_clusters=side, random_state=0).fit_predict(df_X.as_matrix())
        print 'ended X coordinate'
        Y_quant = KMeans(n_clusters=side, random_state=0).fit_predict(df_Y.as_matrix())
        print 'ended Y coordinate'
        print 'Saving on file: ./Dataset/'+dset+'_XYquant_'+str(side)+'.csv'
        pd.DataFrame({'X' : X_quant, 'Y' : Y_quant}).to_csv(path_or_buf='./Dataset/' + dset + '_XYquant_' + str(side) + '.csv', sep=',', na_rep='', float_format=None, columns=None, header=True, index=False, index_label=None, mode='w', encoding=None, compression=None, quoting=None, quotechar='"', line_terminator='\n', chunksize=None, tupleize_cols=False, date_format=None, doublequote=True, escapechar=None, decimal='.')
        index += 1
    print 'Done'


# def ProcessQuantization(ds, intest, side, train=1):
#     if train == 1:
#         path = './Dataset/train' + '_XYquant_' + str(side) + '.csv'
#         if not os.path.exists(path):
#             coordinate_quantization(side)
#         XYQuant, _ = dsFromCSV(path)
#     if train == 0:
#         path = './Dataset/test' + '_XYquant_' + str(side) + '.csv'
#         if not os.path.exists(path):
#             coordinate_quantization(side)
#         XYQuant, _ = dsFromCSV(path)
#
#     for row in XYQuant:
#
#     return ds, intest

def getMinMax():
    ds_train, intest = dsFromCSV("./Dataset/train.csv")
    ds_test, intest_test = dsFromCSV("./Dataset/test.csv")
    min_x = float(ds_train[0]['X'])
    max_x = float(ds_train[0]['X'])
    min_y = float(ds_train[0]['Y'])
    max_y = float(ds_train[0]['Y'])

    n = len(ds_train) + len(ds_test)

    for i in range(len(ds_train)):
        x = float(ds_train[i]['X'])
        y = float(ds_train[i]['Y'])
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

        printProgress(i, n)

    for i in range(len(ds_test)):
        x = float(ds_test[i]['X'])
        y = float(ds_test[i]['Y'])
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

        printProgress(i+len(ds_train), n)

    return min_x, max_x, min_y, max_y