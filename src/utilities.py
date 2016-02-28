import csv
import numpy as np
import urllib
import simplejson
from omgeo import Geocoder

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
		#print query, latitude, longitude
	else:
		latitude, longitude = None, None
		#print query, "<no results>"
	return longitude, latitude
##def get_coordinates(query):
##    g = Geocoder()
##    result = g.geocode(query)
##    return result
##
##print get_coordinates('2000 THOMAS AV, SAN FRANCISCO CA')

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
	if int(100*i/n) >= printProgress.perc:
		print str(printProgress.perc)+'% completed'
		printProgress.perc += 10
	elif i == n-1:
		print '100% completed\n'
		del printProgress.perc

def dsFromCSV(path):
	ds = []
	j = 0
	csvfile = open(path, 'rb')
	n = sum(1 for row in csvfile)
	with open(path,'rb') as csvfile:
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
                        printProgress(j,n)
	return ds, intest

def dsToCSV(path, ds, intest, mode='wb'):
	j = 0
	n = len(ds)
	with open(path, mode) as csvfile:    
		sw = csv.writer(csvfile, delimiter=",")
		sw.writerow(intest)
		for row in ds:
			tmp = []
			for i in intest:
				tmp.append(row[i])
			sw.writerow(tmp)
			printProgress(j,n)
			j += 1


def strToNum(ds, intest, ex):
        converters = []
        new_intest = intest
        for att in ex:
                new_intest.remove(att)
        for i in range(len(new_intest)):
                converters.append(dict())
        new_ds = []
        for row in ds:
                for i in range(len(new_intest)):
                        if row[new_intest[i]] not in converters[i]:
                                converters[i][row[new_intest[i]]] = len(converters[i])

        n = len(ds)
        j = 0
        for row in ds:
                new_row = dict()
                for i in range(len(intest)):
                        if intest[i] not in ex:
                                new_row[intest[i]] = converters[i][row[intest[i]]]
                        else:
                                new_row[intest[i]] = row[intest[i]]
                new_ds.append(new_row)
                printProgress(j,n)
                j += 1
        return new_ds

def getDictCategories(ds, numCategories):
	dictCategories = dict()
	i = 0
	while len(dictCategories) < numCategories:
		category = ds[i]['Category']
		if category not in dictCategories.values():
			dictCategories[len(dictCategories)] = category
		i += 1
	return dictCategories

if (__name__ == "__main__"):
	print "Error"
	exit(1)
