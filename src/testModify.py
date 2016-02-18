import csv

ds = []
with open('./Dataset/test.csv', 'rb') as csvfile:
    sr = csv.reader(csvfile, delimiter=",")
    intest = next(sr)
    for row in sr:
		i = 0
		tmp = {}
		for col in row:
			if(intest[i] != "Id"):
				tmp[intest[i]] = col
			i = i + 1
		ds.append(tmp)
       
del(intest[0])

with open('./Dataset/test_new.csv', 'wb') as csvfile:
    sw = csv.writer(csvfile, delimiter=",")
    sw.writerow(intest)
    for row in ds:
		tmp = [row['Dates'], row['DayOfWeek'], row['PdDistrict'], row['Address'], 
				row['X'], row['Y']]
		sw.writerow(tmp);
