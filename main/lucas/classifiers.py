import ee
import geemap

# SVM Classifier
SVM = ee.Classifier.libsvm(**{
    # Default parameters for SVM
    'kernelType': 'RBF',
    'gamma': 0.5,
    'cost': 10
})

# Cart Classifier
Cart = ee.Classifier.smileCart()

# RandomForest Classifier
RandomForest = ee.Classifier.smileRandomForest(10)
