# Normalizza il test set in uno stato iniziale concordato

from utilities import *
from featureEngineering import *

print "LOADING DATA SET"
ds, intest = dsFromCSV("./Original_Dataset/test.csv");

print "CORRECTING OUTLIERS"
ds = getCorrectCoordinates(ds)

print "SAVING DATA SET"
dsToCSV('./Dataset/test.csv',ds,intest)
