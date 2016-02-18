from utilities import *
import weka.core.jvm as jvm

from weka.core.converters import Loader, Saver

from weka.classifiers import Classifier, Evaluation
from weka.core.classes import Random

jvm.start(max_heap_size="3072m")

loader = Loader(classname="weka.core.converters.ArffLoader")
data = loader.load_file("./Dataset/trainSDR.arff")
data.class_index = 0

classifier = Classifier(classname="weka.classifiers.trees.J48", options=["-C", "0.3"])

evaluation = Evaluation(data)
#evaluation.crossvalidate_model(classifier, data, 10, Random(42))
evaluation.evaluate_train_test_split(classifier, data, 66, Random(42))
print evaluation.summary()

jvm.stop()
