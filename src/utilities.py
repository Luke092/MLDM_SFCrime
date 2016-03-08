import csv
import numpy as np
import urllib
import simplejson


def get_coordinates(query, from_sensor=False):
    googleGeocodeUrl = 'http://maps.googleapis.com/maps/api/geocode/json?'
    query = query.encode('utf-8')
    params = {
        'address': query,
        'sensor': "true" if from_sensor else "false"
    }
    url = googleGeocodeUrl + urllib.urlencode(params)
    json_response = urllib.urlopen(url)
    response = simplejson.loads(json_response.read())
    if response['results']:
        location = response['results'][0]['geometry']['location']
        latitude, longitude = location['lat'], location['lng']
    # print query, latitude, longitude
    else:
        latitude, longitude = None, None
    # print query, "<no results>"
    return longitude, latitude


def multiclass_log_loss(y_true, y_pred, eps=1e-15):
    """Multi class version of Logarithmic Loss metric.
    https://www.kaggle.com/wiki/MultiClassLogLoss

    idea from this post:
    http://www.kaggle.com/c/emc-data-science/forums/t/2149/is-anyone-noticing-difference-betwen-validation-and-leaderboard-error/12209#post12209

    Parameters
    ----------
    y_true : array, shape = [n_samples]
    y_pred : array, shape = [n_samples, n_classes]

    Returns
    -------
    loss : float
    """
    y_true, y_pred = np.asarray(y_true), np.asarray(y_pred)
    predictions = np.clip(y_pred, eps, 1 - eps)

    # normalize row sums to 1
    predictions /= predictions.sum(axis=1)[:, np.newaxis]

    actual = np.zeros(y_pred.shape)
    rows = actual.shape[0]
    actual[np.arange(rows), y_true.astype(int)] = 1
    vsota = np.sum(actual * np.log(predictions))
    return -1.0 / rows * vsota


def printProgress(i, n):
    if not hasattr(printProgress, 'perc'):
        printProgress.perc = 10
    if int(100 * i / n) >= printProgress.perc:
        print str(printProgress.perc) + '% completed'
        printProgress.perc += 10
    elif i == n - 1:
        print '100% completed\n'
        del printProgress.perc


def dsFromCSV(path):
    ds = []
    j = 0
    csvfile = open(path, 'rb')
    n = sum(1 for row in csvfile)
    with open(path, 'rb') as csvfile:
        sr = csv.reader(csvfile, delimiter=",")
        intest = next(sr)
        for row in sr:
            i = 0
            tmp = {}
            for col in row:
                tmp[intest[i]] = col
                i = i + 1
            ds.append(tmp)
            j += 1
            printProgress(j, n)
    return ds, intest


def dsToCSV(path, ds, intest, mode='wb'):
    j = 0
    n = len(ds)
    with open(path, mode) as csvfile:
        sw = csv.writer(csvfile, delimiter=",")
        if mode == 'wb':
            sw.writerow(intest)
        for row in ds:
            tmp = []
            for i in intest:
                tmp.append(row[i])
            sw.writerow(tmp)
            printProgress(j, n)
            j += 1


def strToNum(ds, intest, ex, converter={}):
    if len(converter) == 0:
        new_intest = intest[:]
        try:
            for att in ex:
                new_intest.remove(att)
        except:
            None
        for att in new_intest:
            converter[att] = dict()
        for row in ds:
            for att in new_intest:
                if row[att] not in converter[att]:
                    converter[att][row[att]] = len(converter[att])
    new_ds = []
    n = len(ds)
    j = 0
    for row in ds:
        new_row = dict()
        for att in intest:
            if att not in ex:
                if row[att] in converter[att]:
                    new_row[att] = converter[att][row[att]]
                else:
                    new_row[att] = len(converter[att])
            else:
                new_row[att] = row[att]
        new_ds.append(new_row)
        printProgress(j, n)
        j += 1
    return new_ds, converter


def strToBin(ds, intest, ex, categories={}):
    new_intest = []
    att_values = {}
    ex.append('Category')
    for att in intest:
        if att not in ex:
            att_values[att] = []
    for att in intest:
        if att in ex:
            new_intest.append(att)
        else:
            for row in ds:
                if row[att] not in att_values[att]:
                   att_values[att].append(row[att])
            new_intest = new_intest + att_values[att]

    new_ds = []
    i = 0
    n = len(ds)
    for row in ds:
        new_row = dict()
        for att in intest:
            if att in ex:
                if att == 'Category':
                    new_row[att] = categories.keys()[categories.values().index(row[att])]
                else:
                    new_row[att] = row[att]
            else:
                for value in att_values[att]:
                    new_row[value] = 1 if row[att] == value else 0
        new_ds.append(new_row)
        printProgress(i, n)
        i += 1
    return new_ds, new_intest


def getDictCategories(ds, numCategories):
    dictCategories = dict()
    i = 0
    while len(dictCategories) < numCategories:
        category = ds[i]['Category']
        if category not in dictCategories.values():
            dictCategories[len(dictCategories)] = category
        i += 1
    return dictCategories


def saveSubmission(model, X_test, intest, dictCategories):
    # prob = model.predict_proba(X_test[0:int(len(X_test) / 8)])
    prob = model.predict_proba(np.asanyarray(X_test[0:int(len(X_test) / 8)]))
    submission = []
    Id = 0
    for row in prob:
        l_row = {intest[0]: Id}
        for i in range(0, len(row)):
            l_row[dictCategories[i]] = prob[Id][i]
        Id += 1
        submission.append(l_row)

    print 'SAVING SUBMISSION 1/8'
    dsToCSV('./Dataset/submission.csv', submission, intest)

    del prob
    del submission
    del l_row

    limits = [int(i * len(X_test) / 8) for i in range(1, 9)]
    for k in range(0, len(limits) - 1):
        submission = []
        # prob = model.predict_proba(X_test[limits[k]:limits[k + 1]])
        prob = model.predict_proba(np.asarray(X_test[limits[k]:limits[k + 1]]))
        for row in prob:
            l_row = {intest[0]: Id}
            for i in range(0, len(row)):
                l_row[dictCategories[i]] = prob[Id - limits[k]][i]
            Id += 1
            submission.append(l_row)
        print 'SAVING SUBMISSION', str(k + 2) + '/8'
        dsToCSV('./Dataset/submission.csv', submission, intest, 'ab')


if (__name__ == "__main__"):
    print "Error"
    exit(1)
