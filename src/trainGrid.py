from utilities import *
from featureEngineering import *

ds, intest = dsFromCSV('./Dataset/train_prep.csv')
ds = processGrid(ds, intest, gridSide=1000, isTrain=True)

for i in range(0,len(intest)):
	if intest[i] == "Address":
		del(intest[i])
		break
		
ex = ['X', 'Y']
ds_new = strToNum(ds,intest,ex)

dsToCSV('./Dataset/trainGrid.csv', ds_new, intest)
