import sys
from utilities import *
from featureEngineering import *
from sklearn.metrics import accuracy_score
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.naive_bayes import GaussianNB, BernoulliNB, MultinomialNB
from sklearn.linear_model import LogisticRegression
# from sknn.mlp import Classifier, Layer
import numpy as np

NUM_CATEGORIES = 39
GRIDSIDE = 100
TO_REMOVE = ['Dates']
TO_PROCESS = 'YMHm'

def sdr_process(ds,intest):
    print 'PROCESSING SDR ON TRAIN SET'
    d_set, d_intest = processSDR(ds, intest)
    return d_set, d_intest

def date_process(ds,intest):
    print 'PROCESSING DATE ON TRAIN SET'
    d_set, d_intest, ex = processDate(ds, intest, TO_PROCESS)
    return d_set, d_intest, ex

def grid_process(ds):
    print 'PROCESSING GRID ON TRAIN SET'
    d_set = processGrid(ds, GRIDSIDE)
    return d_set

def cross_process(ds, intest):
    print 'PROCESSING CROSS ON TRAIN SET'
    d_set, d_intest = processCross(ds, intest)
    return d_set, d_intest

def street_process(ds):
    print 'PROCESSING STREET ON TRAIN SET'
    d_set = address_to_type(ds)
    return d_set

def day_process(ds, intest):
    print 'PROCESSING DAY ON TRAIN SET'
    d_set, d_intest = processDay(ds, intest)
    return d_set, d_intest




def main_prog(engineering):
    print 'LOADING TRAIN SET'
    train_set, train_intest = dsFromCSV('./Dataset/train.csv')

    dictCategories = getDictCategories(train_set, NUM_CATEGORIES)
    cat = dictCategories.values()
    cat.sort()
    intest = ['Id']
    intest += cat
    ex=[]

    ##########################################################################
    if (int(engineering[0]) == 1):
        train_set, train_intest = sdr_process(train_set,train_intest)

    elif (int(engineering[0]) == 2):
        train_set, train_intest, ex = date_process(train_set,train_intest)

    elif (int(engineering[0]) == 3):
        train_set, train_intest = sdr_process(train_set, train_intest)
        train_set, train_intest, ex = date_process(train_set, train_intest)

    ##########################################################################
    if (int(engineering[1]) == 1):
        train_set = grid_process(train_set)

    #########################################################################
    if (int(engineering[2]) == 1):
        train_set, train_intest = cross_process(train_set, train_intest)

    elif (int(engineering[2]) == 2):
        train_set = address_to_type(train_set)

    elif (int(engineering[2]) == 3):
        train_set, train_intest = cross_process(train_set, train_intest)
        train_set = address_to_type(train_set)

    #########################################################################
    if (int(engineering[3]) == 1):
        train_set, train_intest = day_process(train_set, train_intest)

    #########################################################################

    # Remove attributes

    removeAtts(train_set, train_intest, TO_REMOVE)

    #########################################################################

    ex += ['X', 'Y']
    print 'CONVERTING TRAIN SET ATTS IN NUMERIC'
    train_set, converter = strToNum(train_set, train_intest, ex)

    #########################################################################

    # print 'CONVERTING TRAIN SET ATTS IN BINARY'
    # train_set, train_intest = strToBin(train_set, train_intest, ex, dictCategories)

    # print 'SAVING TRAIN SET'
    # dsToCSV('./Dataset/trainBin.csv', train_set, train_intest)

    #########################################################################

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

    clf1 = tree.DecisionTreeClassifier(criterion='gini',min_samples_split=250)
    clf2 = GaussianNB()
    clf3 = tree.DecisionTreeClassifier(criterion='entropy',min_samples_leaf=39)
    clf4 = tree.DecisionTreeClassifier(criterion='gini',max_depth=4)
    # clf4 = BernoulliNB()
    # clf5 = MultinomialNB()
    # clf = LogisticRegression(C=.01)
    # clf = RandomForestClassifier(n_jobs=-1, n_estimators=50,max_depth=16)
    # clf4 = Classifier(
    #     layers=[
    #         Layer("Tanh", units=100),
    #         Layer("Sigmoid", units=100),
    #         Layer('Softmax')],
    #     learning_rate=0.1,
    #     learning_rule='momentum',
    #     learning_momentum=0.9,
    #     batch_size=100,
    #     valid_size=0.01,
    #     n_stable=2,
    #     n_iter=20,
    #     verbose=True)
    clf = VotingClassifier(estimators=[('1',clf1),
                                       ('2',clf2),
                                       ('3',clf3),
                                       ('4',clf4),
                                       # ('5',clf5)
                                       ],
                           voting='soft',
                           weights=[5,2,4,1]
                           )

    print 'FITTING MODEL'
    # model = clf.fit(X_train_set,Y_train_set)
    # Y_predict = model.predict(X_test_set)
    # prob = model.predict_proba(X_test_set)

    model = clf.fit(np.asarray(X_train_set), np.asanyarray(Y_train_set))
    Y_predict = model.predict(np.asarray(X_test_set))
    prob = model.predict_proba(np.asarray(X_test_set))

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

       ##########################################################################
    if (int(engineering[0]) == 1):
        test_set, test_intest = sdr_process(test_set,test_intest)

    elif (int(engineering[0]) == 2):
        test_set, test_intest, ex = date_process(test_set,test_intest)

    elif (int(engineering[0]) == 3):
        test_set, test_intest = sdr_process(test_set, test_intest)
        test_set, test_intest, ex = date_process(test_set, test_intest)

    ##########################################################################
    if (int(engineering[1]) == 1):
        test_set = grid_process(test_set)

    #########################################################################
    if (int(engineering[2]) == 1):
        test_set, test_intest = cross_process(test_set, test_intest)

    elif (int(engineering[2]) == 2):
        test_set = address_to_type(test_set)

    elif (int(engineering[2]) == 3):
        test_set, test_intest = cross_process(test_set, test_intest)
        test_set = address_to_type(test_set)

    #########################################################################
    if (int(engineering[3]) == 1):
        test_set, test_intest = day_process(test_set, test_intest)

    #########################################################################

    # Remove attributes

    removeAtts(test_set, test_intest, TO_REMOVE)

    #########################################################################

    print 'FITTING MODEL'
    # model = clf.fit(X_train, Y_train)
    model = clf.fit(np.asarray(X_train), np.asanyarray(Y_train))

    del X_train
    del Y_train

    ########################################################################
    ex.append('Id')

    ex += ['X', 'Y']
    print 'CONVERTING TEST SET ATTS IN NUMERIC'
    test_set, _ = strToNum(test_set, test_intest, ex, converter)

    ########################################################################

    # print 'CONVERTING TEST SET ATTS IN BINARY'
    # test_set, test_intest = strToBin(test_set, test_intest, ex)

    # print 'SAVING TEST SET'
    # dsToCSV('./Dataset/testBin.csv', test_set, test_intest)

    ########################################################################

    for row in test_set:
        l_row = []
        for i in test_intest:
            if i != 'Id':
                l_row.append(row[i])
        X_test.append(l_row)

    del test_set

    saveSubmission(model, X_test, intest, dictCategories)

if (__name__ == "__main__"):
    if (len(sys.argv) > 1):
        engineering = sys.argv[1:]
        main_prog(engineering)
    else:
        main_prog([1, 1, 1, 1])
