import csv
import weka.core.jvm as jvm
from weka.core.converters import Loader, Saver

def dsFromCSV(path):
	ds = []
	with open(path,'rb') as csvfile:
		sr = csv.reader(csvfile, delimiter=",")
		intest = next(sr)
		for row in sr:
			i = 0
			tmp = {}
			for col in row:
				tmp[intest[i]] = col
				i = i + 1
			ds.append(tmp)
	return ds, intest

def dsToCSV(path, ds, intest):
	with open(path, 'wb') as csvfile:
		sw = csv.writer(csvfile, delimiter=",")
		sw.writerow(intest)
		for row in ds:
			tmp = []
			for i in intest:
				tmp.append(row[i])
			sw.writerow(tmp);
			
def convert_to_arff(csv_path, arff_path):
	jvm.start()
	loader = Loader(classname="weka.core.converters.CSVLoader")
	data = loader.load_file(csv_path)
	saver = Saver(classname="weka.core.converters.ArffSaver")
	saver.save_file(data, arff_path)
	jvm.stop()



if (__name__ == "__main__"):
	print "Error"
	exit(1)
