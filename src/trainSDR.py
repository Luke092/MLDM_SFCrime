# Preleva le prime n istanze e sostituisce l'attributo "Dates"
# con gli attributi "Season" e "Daily range"



from utilities import *
from featureEngineering import *

ds, intest = dsFromCSV('./Dataset/train.csv')
new_ds, new_intest = processSDR(ds, intest)
        
#i = 0	
#for el in intest:
#	if(el == "X"):
#		del(intest[i])
#	i = i + 1
	
#i = 0	
#for el in intest:
#	if(el == "Y"):
#		del(intest[i])
#	i = i + 1
	
#i = 0	
#for el in intest:
#	if(el == "PdDistrict"):
#		del(intest[i])
#	i = i + 1
      
dsToCSV('./Dataset/trainSDR.csv', new_ds, new_intest)
