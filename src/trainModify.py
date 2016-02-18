from utilities import *

ds, intest = dsFromCSV('./Dataset/train.csv')
dellist = []
for i in range(0, len(intest)-1):
	if (intest[i] == "Descript" or intest[i] == "Resolution"):
		del(intest[i])
		i = i - 1
	if(i == len(intest) -1):
		break

new_ds = []
for i in range(0,1000):
	new_ds.append(ds[i])
	
dsToCSV('./Dataset/train_new.csv',new_ds,intest)
