from utilities import *
from featureEngineering import *
from sklearn import tree
from sklearn.naive_bayes import GaussianNB
import numpy as np
##########################################################################

##train_set, train_intest = dsFromCSV('./Dataset/train.csv')
##test_set, test_intest = dsFromCSV('./Dataset/test.csv')
##
##train_set, train_intest = processSDR(train_set, train_intest)
##test_set, test_intest = processSDR(test_set, test_intest)
##
##dsToCSV('./Dataset/trainSDR.csv', train_set, train_intest)
##dsToCSV('./Dataset/testSDR.csv', test_set, test_intest)

##########################################################################

##train_set, train_intest = dsFromCSV('./Dataset/trainSDR.csv')
##test_set, test_intest = dsFromCSV('./Dataset/testSDR.csv')
##num_categories = 39
##
##gridSide = 200
##train_set = processGrid(train_set, train_intest, gridSide)
##test_set = processGrid(test_set, test_intest, gridSide)
##
##dsToCSV('./Dataset/trainGrid.csv', train_set, train_intest)
##dsToCSV('./Dataset/testGrid.csv', test_set, test_intest)

#########################################################################

train_set, train_intest = dsFromCSV('./Dataset/trainGrid.csv')
num_categories = 39
dictCategories = getDictCategories(train_set, num_categories)
cat = dictCategories.values()
cat.sort()
intest = ['Id']
intest += cat
ex = ['X', 'Y']
train_set = strToNum(train_set, train_intest, ex)

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
    
test_set, test_intest = dsFromCSV('./Dataset/testGrid.csv')

#clf = tree.DecisionTreeClassifier(criterion='entropy',min_samples_split=500)
clf = GaussianNB()
clf = clf.fit(X_train,Y_train)

del train_set
del X_train
del Y_train

test_set = strToNum(test_set, test_intest, ex)

for row in test_set:
    l_row = []
    for i in test_intest:
        l_row.append(row[i])
    X_test.append(l_row)

del test_set

prob = clf.predict_proba(X_test[0:int(len(X_test)/4)])
limits = [int(len(X_test)/4), int(len(X_test)/2), int(3*len(X_test)/4), len(X_test)-1]
for i in range(0,3):
    prob = np.concatenate(prob, clf.predict_proba(X_test[limits[i]+1:limits[i+1]]))

