import sys
from utilities import *
from featureEngineering import *
from sklearn import tree
from sklearn.naive_bayes import GaussianNB
import numpy as np

NUM_CATEGORIES = 39
GRIDSIDE = 200

def main_prog(engineering):

	print 'LOADING TRAIN SET'
	train_set, train_intest = dsFromCSV('./Dataset/train.csv')
	toRemove = ['X','Y']
	removeAtts(train_set, train_intest, toRemove)
	print 'LOADING TEST SET'
	test_set, test_intest = dsFromCSV('./Dataset/test.csv')
	removeAtts(test_set, test_intest, toRemove)

	##########################################################################
	if(int(engineering[0]) == 1):

		print 'PROCESSING SDR ON TRAIN SET'
		train_set, train_intest = processSDR(train_set, train_intest)
		print 'PROCESSING SDR ON TEST SET'
		test_set, test_intest = processSDR(test_set, test_intest)

		print 'SAVING TRAIN SET'
		dsToCSV('./Dataset/trainSDR.csv', train_set, train_intest)
		print 'SAVING TEST SET'
		dsToCSV('./Dataset/testSDR.csv', test_set, test_intest)

	##########################################################################
	if(int(engineering[1]) == 1):
		# print 'LOADING TRAIN SET'
		# train_set, train_intest = dsFromCSV('./Dataset/trainSDR.csv')
		# print 'LOADING TEST SET'
		# test_set, test_intest = dsFromCSV('./Dataset/testSDR.csv')

		print 'PROCESSING GRID ON TRAIN SET'
		train_set = processGrid(train_set, GRIDSIDE)
		print 'PROCESSING GRID ON TEST SET'
		test_set = processGrid(test_set, GRIDSIDE)

		print 'SAVING TRAIN SET'
		dsToCSV('./Dataset/trainGrid.csv', train_set, train_intest)
		print 'SAVING TEST SET'
		dsToCSV('./Dataset/testGrid.csv', test_set, test_intest)

	#########################################################################
	if (int(engineering[2]) == 1):
		# print 'LOADING TRAIN SET'
		# train_set, train_intest = dsFromCSV('./Dataset/trainGrid.csv')
		# print 'LOADING TEST SET'
		# test_set, test_intest = dsFromCSV('./Dataset/testGrid.csv')

		print 'PROCESSING CROSS ON TRAIN SET'
		train_set, train_intest = processCross(train_set, train_intest)
		print 'PROCESSING CROSS ON TEST SET'
		test_set, test_intest = processCross(test_set, test_intest)

		print 'SAVING TRAIN SET'
		dsToCSV('./Dataset/trainCross.csv', train_set, train_intest)
		print 'SAVING TEST SET'
		dsToCSV('./Dataset/testCross.csv', test_set, test_intest)

	#########################################################################

	# print 'LOADING TRAIN SET'
	# train_set, train_intest = dsFromCSV('./Dataset/trainCross.csv')

	dictCategories = getDictCategories(train_set, NUM_CATEGORIES)
	cat = dictCategories.values()
	cat.sort()
	intest = ['Id']
	intest += cat
	ex = ['X', 'Y']
	print 'CONVERTING TRAIN SET ATTS IN NUMERIC'
	train_set, converter = strToNum(train_set, train_intest, ex)

	X_train = []
	Y_train = []
	X_test = []

	for row in train_set:
		l_row = []
		for i in train_intest:
			if(i != "Category"):
				l_row.append(row[i])
			else:
				Y_train.append(row[i])
		X_train.append(l_row)

	del train_set

	# clf = tree.DecisionTreeClassifier(criterion='gini',min_samples_split=80)
	clf = GaussianNB()

	print 'FITTING MODEL'
	clf = clf.fit(X_train,Y_train)

	del X_train
	del Y_train

##	print 'LOADING TEST SET'
##	test_set, test_intest = dsFromCSV('./Dataset/testCross.csv')

	print 'CONVERTING TEST SET ATTS IN NUMERIC'
	ex.append('Id')
	test_set, _ = strToNum(test_set, test_intest, ex, converter)

	for row in test_set:
		l_row = []
		for i in test_intest:
			if i != 'Id':
				l_row.append(row[i])
		X_test.append(l_row)

	del test_set

	prob = clf.predict_proba(X_test[0:int(len(X_test)/8)])
	submission = []
	Id = 0
	for row in prob:
		l_row = {intest[0] : Id}
		for i in range(0,len(row)):
			l_row[dictCategories[i]] = prob[Id][i]
		Id += 1
		submission.append(l_row)

	print 'SAVING SUBMISSION 1/8'
	dsToCSV('./Dataset/submission.csv', submission, intest)

	del prob
	del submission
	del l_row

	limits = [int(i*len(X_test)/8) for i in range(1,9)]
	for k in range(0,len(limits)-1):
		submission = []
		prob = clf.predict_proba(X_test[limits[k]:limits[k+1]])
		for row in prob:
			l_row = {intest[0] : Id}
			for i in range(0,len(row)):
				l_row[dictCategories[i]] = prob[Id-limits[k]][i]
			Id += 1
			submission.append(l_row)
		print 'SAVING SUBMISSION', str(k+2) + '/8'
		dsToCSV('./Dataset/submission.csv', submission, intest, 'ab')

if(__name__ == "__main__"):
	if(len(sys.argv) == 4):
		engineering = sys.argv[1:]
		main_prog(engineering)
	else:
		main_prog([1,1,1])
