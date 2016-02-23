from utilities import *
from sklearn import tree
from sklearn.naive_bayes import GaussianNB
from sklearn.feature_extraction import DictVectorizer, FeatureHasher

ds, intest = dsFromCSV('./Dataset/trainSDR.csv')

ds_new = [ds[i] for i in range(0,10)]


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
X_test_set = [X[i] for i in range(limit+1, len(ds))]
Y_train_set = [Y[i] for i in range(0,limit)]
Y_test_set = [Y[i] for i in range(limit+1, len(ds))]

enc = FeatureHasher(input_type='string')
t = enc.fit_transform(Y)
print t.toarray()

exit(0)

#clf = tree.DecisionTreeClassifier()
#clf = clf.fit(X_train_set,Y_train_set)

#Y_predict = clf.predict(X_test_set)

clf = GaussianNB()
Y_predict = clf.fit(X_train_set,Y_train_set).predict(X_test_set)


#print Y_predict
