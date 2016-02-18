import sys
import weka.core.jvm as jvm
from weka.core.converters import Loader, Saver
			
def convert_to_arff(csv_path, arff_path):
	jvm.start()
	loader = Loader(classname="weka.core.converters.CSVLoader")
	data = loader.load_file(csv_path)
	saver = Saver(classname="weka.core.converters.ArffSaver")
	saver.save_file(data, arff_path)
	jvm.stop()


if (len(sys.argv) == 3):
	convert_to_arff(sys.argv[1],sys.argv[2])
