import sys
from utilities import *
from featureEngineering import *
from sklearn.metrics import accuracy_score
from sklearn import tree
from sklearn.naive_bayes import GaussianNB
import numpy as np

NUM_CATEGORIES = 39
GRIDSIDE = 200


def main_prog(engineering):
    print 'LOADING TRAIN SET'
    train_set, train_intest = dsFromCSV('./Dataset/train.csv')

    dictCategories = getDictCategories(train_set, NUM_CATEGORIES)
    cat = dictCategories.values()
    cat.sort()
    intest = ['Id']
    intest += cat

    toRemove = ['Address']
    removeAtts(train_set, train_intest, toRemove)

    ##########################################################################
    if (int(engineering[0]) == 1):
        print 'PROCESSING SDR ON TRAIN SET'
        train_set, train_intest = processSDR(train_set, train_intest)

        print 'SAVING TRAIN SET'
        dsToCSV('./Dataset/trainSDR.csv', train_set, train_intest)

    ##########################################################################
    if (int(engineering[1]) == 1):
        print 'PROCESSING GRID ON TRAIN SET'
        train_set = processGrid(train_set, GRIDSIDE)

        print 'SAVING TRAIN SET'
        dsToCSV('./Dataset/trainGrid.csv', train_set, train_intest)

    #########################################################################
    if (int(engineering[2]) == 1):
        print 'PROCESSING CROSS ON TRAIN SET'
        train_set, train_intest = processCross(train_set, train_intest)

        print 'SAVING TRAIN SET'
        dsToCSV('./Dataset/trainCross.csv', train_set, train_intest)

    #########################################################################

    ex = ['X', 'Y']
    print 'CONVERTING TRAIN SET ATTS IN NUMERIC'
    train_set, converter = strToNum(train_set, train_intest, ex)

    X_train = []
    Y_train = []
    X_test = []

    for row in train_set:
        l_row = []
        for i in train_intest:
            if (i != "Category"):
                l_row.append(row[i])
            else:
                Y_train.append(row[i])
        X_train.append(l_row)

    del train_set

    X_train_set = []
    X_test_set = []
    Y_train_set = []
    Y_test_set = []

    for i in range(len(X_train)):
        if (i % 3 == 0):
            X_test_set.append(X_train[i])
            Y_test_set.append(Y_train[i])
        else:
            X_train_set.append(X_train[i])
            Y_train_set.append(Y_train[i])

    # clf = tree.DecisionTreeClassifier(criterion='gini',min_samples_split=80)
    clf = GaussianNB()

    print 'FITTING MODEL'
    model = clf.fit(X_train_set, Y_train_set)
    Y_predict = model.predict(X_test_set)
    prob = model.predict_proba(X_test_set)

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

    wantSubmit = '0'
    while wantSubmit not in 'yn':
        wantSubmit = raw_input('Do you want to proceed with submission? (y/n): ')
        if wantSubmit == 'n':
            exit(0)

    ####################################################################################################################
    ####################################################################################################################

    print 'LOADING TEST SET'
    test_set, test_intest = dsFromCSV('./Dataset/test.csv')
    removeAtts(test_set, test_intest, toRemove)

    ##########################################################################
    if (int(engineering[0]) == 1):
        print 'PROCESSING SDR ON TEST SET'
        test_set, test_intest = processSDR(test_set, test_intest)

        print 'SAVING TEST SET'
        dsToCSV('./Dataset/testSDR.csv', test_set, test_intest)

    ##########################################################################
    if (int(engineering[1]) == 1):
        print 'PROCESSING GRID ON TEST SET'
        test_set = processGrid(test_set, GRIDSIDE)

        print 'SAVING TEST SET'
        dsToCSV('./Dataset/testGrid.csv', test_set, test_intest)

    #########################################################################
    if (int(engineering[2]) == 1):
        print 'PROCESSING CROSS ON TEST SET'
        test_set, test_intest = processCross(test_set, test_intest)

        print 'SAVING TEST SET'
        dsToCSV('./Dataset/testCross.csv', test_set, test_intest)

    #########################################################################
    print 'FITTING MODEL'
    model = clf.fit(X_train, Y_train)

    del X_train
    del Y_train

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

    saveSubmission(model, X_test, intest, dictCategories)

if (__name__ == "__main__"):
    if (len(sys.argv) == 4):
        engineering = sys.argv[1:]
        main_prog(engineering)
    else:
        main_prog([1, 1, 1])