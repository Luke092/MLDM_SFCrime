from utilities import *
from sklearn import tree
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import Perceptron, SGDClassifier

from sklearn.metrics import accuracy_score


ds, intest = dsFromCSV('./Dataset/trainGrid.csv')

ex = ['X', 'Y']
ds = strToNum(ds, intest, ex)
#dsToCSV('./Dataset/trainNUM.csv', ds, intest)

X = []
Y = []
ds = ds[0:450000]
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

del ds

clf = tree.DecisionTreeClassifier(criterion='entropy',min_samples_split=15)
#clf = RandomForestClassifier(n_estimators=2,max_depth=5,min_samples_split=500)
#clf = Perceptron()
#clf = SGDClassifier()
#clf = GaussianNB()

clf = clf.fit(X_train_set,Y_train_set)

Y_predict = clf.predict(X_test_set)
prob = clf.predict_proba(X_test_set)

##count = 0
##for i in range(len(prob)):
##      if prob[i][Y_test_set[i]] == 0:
##              count += 1
##print 1-float(count)/len(ds)

accuracy = accuracy_score(Y_test_set, Y_predict)
print 'Accuracy: ' + str(accuracy)

score = multiclass_log_loss(Y_test_set, prob)
print str(score)
