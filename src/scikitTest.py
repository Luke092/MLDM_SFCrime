from utilities import *
from sklearn import tree
from featureEngineering import *
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import Perceptron, SGDClassifier

from sklearn.metrics import accuracy_score

NUM_CATEGORIES = 39
GRIDSIDE = 200

def main_prog(engineering):
	
	print 'LOADING TRAIN SET'
	ds, intest = dsFromCSV('./Dataset/train.csv')
	
	##########################################################################
	if(int(engineering[0]) == 1):
		
		print 'PROCESSING SDR ON TRAIN SET'
		ds, intest = processSDR(ds, train_intest)
		
		# print 'SAVING TRAIN SET'
		# dsToCSV('./Dataset/trainSDR.csv', ds, train_intest)

	##########################################################################
	if(int(engineering[1]) == 1):
		# print 'LOADING TRAIN SET'
		# ds, train_intest = dsFromCSV('./Dataset/trainSDR.csv')
		print 'PROCESSING GRID ON TRAIN SET'
		ds = processGrid(ds, GRIDSIDE)
		#
		# print 'SAVING TRAIN SET'
		# dsToCSV('./Dataset/trainGrid.csv', ds, train_intest)

	#########################################################################
	if (int(engineering[2]) == 1):
		# print 'LOADING TRAIN SET'
		# train_set, train_intest = dsFromCSV('./Dataset/trainGrid.csv')
		#
		print 'PROCESSING CROSS ON TRAIN SET'
		ds, train_intest = processCross(ds, intest)
		#
		# print 'SAVING TRAIN SET'
		# dsToCSV('./Dataset/trainCross.csv', train_set, train_intest)

	#########################################################################

	# print 'LOADING TRAIN SET'
	# ds, train_intest = dsFromCSV('./Dataset/trainGrid.csv')

	ex = ['X', 'Y']
	print 'CONVERTING DATA SET ATTS IN NUMERIC'
	ds = strToNum(ds, intest, ex)

	X = []
	Y = []
	for row in ds:
			l_row = []
			for i in intest:
					if(i != "Category"):
							l_row.append(row[i])
					else:
							Y.append(row[i])
			X.append(l_row)
			
	limit = int(round(len(ds)*0.66))


	X_train_set = [X[i] for i in range(0,limit)]
	X_test_set = [X[i] for i in range(limit, len(ds))]
	Y_train_set = [Y[i] for i in range(0,limit)]
	Y_test_set = [Y[i] for i in range(limit, len(ds))]

	del ds

	clf = tree.DecisionTreeClassifier(criterion='gini',min_samples_split=2500,max_depth=8)
	#clf = RandomForestClassifier(n_estimators=2,max_depth=5,min_samples_split=500)
	#clf = Perceptron()
	#clf = SGDClassifier()
	# clf = GaussianNB()

	clf = clf.fit(X_train_set,Y_train_set)

	Y_predict = clf.predict(X_test_set)
	prob = clf.predict_proba(X_test_set)

	del X_train_set
	del X_test_set
	del Y_train_set

	##count = 0
	##for i in range(len(prob)):
	##      if prob[i][Y_test_set[i]] == 0:
	##              count += 1
	##print 1-float(count)/len(ds)

	accuracy = accuracy_score(Y_test_set, Y_predict)
	print 'Accuracy: ' + str(accuracy)

	##del Y_predict

	score = multiclass_log_loss(Y_test_set, prob)
	print 'Score: ' + str(score)

if(__name__ == "__main__"):
	if(len(sys.argv) == 4):
		engineering = sys.argv[1:]
		main_prog(engineering)
	else:
		main_prog([1,1,1])
