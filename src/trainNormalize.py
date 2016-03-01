# Normalizza il training set in uno stato iniziale concordato

from utilities import *
from featureEngineering import *

print "LOADING DATA SET"
ds, intest = dsFromCSV('./Original_Dataset/train.csv')

intest.remove("Descript")
intest.remove("Resolution")
intest.remove("Category")
intest.append("Category")

print "CORRETCTING OUTLIERS"
ds = getCorrectCoordinates(ds)

print "SAVING DATA SET"
dsToCSV('./Dataset/train.csv',ds,intest)
