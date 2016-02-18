# Normalizza il training set in uno stato iniziale concordato

from utilities import *

ds, intest = dsFromCSV('./Original_Dataset/train.csv')

i = 0	
for el in intest:
	if(el == "Descript"):
		del(intest[i])
	i = i + 1
	
i = 0	
for el in intest:
	if(el == "Resolution"):
		del(intest[i])
	i = i + 1
	
i = 0	
for el in intest:
	if(el == "Category"):
		del(intest[i])
		intest.insert(len(intest),el)
	i = i + 1

dsToCSV('./Dataset/train.csv',ds,intest)
