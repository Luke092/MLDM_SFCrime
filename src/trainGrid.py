from utilities import *

ds, intest = dsFromCSV('./Dataset/train_prep.csv')
ds_new = []

limit_X_min = -122.511076
limit_X_max = -122.365671
limit_Y_min = 37.707777
limit_Y_max = 37.836333

min_x = float(ds[0]['X'])
max_x = float(ds[0]['X'])
min_y = float(ds[0]['Y'])
max_y = float(ds[0]['Y'])

for i in range(1,len(ds)):
	x = float(ds[i]['X'])
	y = float(ds[i]['Y'])
	x_ok = 0
	y_ok = 0
	if (limit_X_min <= x <= limit_X_max):
		if x < min_x:
			min_x = x
		if x > max_x:
			max_x = x
		x_ok = 1
	if (limit_Y_min <= y <= limit_Y_max):
		if y < min_y:
			min_y = y
		if y > max_y:
			max_y = y
		y_ok = 1
	if (x_ok == 1 and y_ok == 1):
		ds_new.append(ds[i])
		
ds = ds_new
# n = numero di celle
n = 1000
step_x = (max_x - min_x)/n
step_y = (max_y - min_y)/n

for row in ds:
	row['X'] = str(round((float(row['X']) - min_x)/step_x))
	row['Y'] = str(round((float(row['Y']) - min_y)/step_y))

for i in range(0,len(intest)):
	if intest[i] == "Address":
		del(intest[i])
		break
		
ex = ['X', 'Y']
ds_new = strToNum(ds,intest,ex)

dsToCSV('./Dataset/trainGrid.csv', ds_new, intest)
