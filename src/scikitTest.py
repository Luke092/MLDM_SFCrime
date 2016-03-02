import sys
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
    toRemove = ['X','Y']
    ds, intest = removeAtts(ds, intest, ['X','Y'])

    ##########################################################################
    if (int(engineering[0]) == 1):
        print 'PROCESSING SDR ON TRAIN SET'
        ds, intest = processSDR(ds, intest)

        print 'SAVING TRAIN SET'
        dsToCSV('./Dataset/trainSDR.csv', ds, intest)

    ##########################################################################
    if (int(engineering[1]) == 1):
        # print 'LOADING TRAIN SET'
        # ds, intest = dsFromCSV('./Dataset/trainSDR.csv')
        print 'PROCESSING GRID ON TRAIN SET'
        ds = processGrid(ds, GRIDSIDE)

        print 'SAVING TRAIN SET'
        dsToCSV('./Dataset/trainGrid.csv', ds, intest)

    #########################################################################
    if (int(engineering[2]) == 1):
        # print 'LOADING TRAIN SET'
        # ds, intest = dsFromCSV('./Dataset/trainGrid.csv')
        #
        print 'PROCESSING CROSS ON TRAIN SET'
        ds, intest = processCross(ds, intest)

        print 'SAVING TRAIN SET'
        dsToCSV('./Dataset/trainCross.csv', ds, intest)

    #########################################################################

    # print 'LOADING TRAIN SET'
    # ds, intest = dsFromCSV('./Dataset/trainCross.csv')

    ex = ['X', 'Y']
    print 'CONVERTING DATA SET ATTS IN NUMERIC'
    ds, _ = strToNum(ds, intest, ex)

    X = []
    Y = []
    for row in ds:
        l_row = []
        for i in intest:
            if (i != "Category"):
                l_row.append(row[i])
            else:
                Y.append(row[i])
        X.append(l_row)

    del ds

    X_train_set = []
    X_test_set = []
    Y_train_set = []
    Y_test_set = []

    for i in range(len(X)):
        if (i % 3 == 0):
            X_test_set.append(X[i])
            Y_test_set.append(Y[i])
        else:
            X_train_set.append(X[i])
            Y_train_set.append(Y[i])

    # print "% train = " + str(float(len(X_train_set))/len(X))
    # print "% test = " + str(float(len(X_test_set))/len(X))

    # clf = tree.DecisionTreeClassifier(criterion='gini', min_samples_split=80)
    # clf = RandomForestClassifier(n_estimators=2,max_depth=5,min_samples_split=500)
    # clf = Perceptron()
    # clf = SGDClassifier()
    clf = GaussianNB()

    clf = clf.fit(X_train_set, Y_train_set)

    Y_predict = clf.predict(X_test_set)
    prob = clf.predict_proba(X_test_set)

    del X_train_set
    del X_test_set
    del Y_train_set

    accuracy = accuracy_score(Y_test_set, Y_predict)
    accuracy = '{0:.5f}'.format(accuracy)
    print 'Accuracy:', accuracy

    del Y_predict

    score = multiclass_log_loss(Y_test_set, prob)
    score = '{0:.5f}'.format(score)
    print 'Score:', score

if (__name__ == "__main__"):
    if (len(sys.argv) == 4):
        engineering = sys.argv[1:]
        main_prog(engineering)
    else:
        main_prog([1, 1, 1])
