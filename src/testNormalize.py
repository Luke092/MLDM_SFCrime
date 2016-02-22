# Normalizza il test set in uno stato iniziale concordato

from utilities import *

ds, intest = dsFromCSV("./Original_Dataset/test.csv");
       
del(intest[0])

dsToCSV('./Dataset/test.csv',ds,intest)
