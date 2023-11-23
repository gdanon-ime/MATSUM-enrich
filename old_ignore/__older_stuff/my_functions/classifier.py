print("Classifier Imported")

import ee

bands = ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B10', 'B11']
# bands = image.bandNames()

# SVM Classifier
classifier = ee.Classifier.libsvm(**{
    # Default parameters for SVM
    'kernelType': 'RBF',
    'gamma': 0.5,
    'cost': 10
})

def train_classifier(image, trainingGcp):
    # Create the training data
    # by getting values for all pixels
    training = image.sampleRegions(**{
        'collection': trainingGcp,
        # Here I define which property im gonna use in the classification
        'properties': ['landcover'],
        'scale': 30
    })

    # Train classifier
    trained = classifier.train(**{
        'features': training,
        'classProperty': 'landcover',
        'inputProperties': bands
        })

    return trained

def test_classification(image_classified, validationGcp):
    test = image_classified.sampleRegions(**{
    'collection': validationGcp,
    'properties': ['landcover'],
    'scale': 30
    })

    testConfusionMatrix = test.errorMatrix('landcover', 'classification')

    print('Confusion Matrix', testConfusionMatrix.getInfo())
    print('Test Accuracy', testConfusionMatrix.accuracy().getInfo())
    
    