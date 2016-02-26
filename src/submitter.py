from utilities import *
from featureEngineering import *
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

train_set, train_intest = dsFromCSV('./Dataset/trainSDR.csv')
test_set, test_intest = dsFromCSV('./Dataset/testSDR.csv')

gridSide = 200
train_set = processGrid(train_set, train_intest, gridSide, isTrain=True)
test_set = processGrid(test_set, test_intest, gridSide, isTrain=False)

dsToCSV('./Dataset/trainGrid.csv', train_set, train_intest)
dsToCSV('./Dataset/testGrid.csv', test_set, test_intest)
