import ee
import geemap

#-----------------------------> Data constants to use: Italy and the Classifier

countries = ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017")
Italy = countries.filter(ee.Filter.eq('country_na', 'Italy'))

classifier = ee.Classifier.libsvm(**{
    # Default parameters for SVM
    'kernelType': 'RBF',
    'gamma': 0.5,
    'cost': 10
})

#-------------------------------> Utility functions

# A function to extract image pixel neighborhood statistics for a given region.
# REF: https://developers.google.com/earth-engine/tutorials/community/extract-raster-values-for-points

def random_points():
    random_points = ee.FeatureCollection.randomPoints(
    region=Italy, points=2000, seed=0, maxError=1
    )   
    return ee.FeatureCollection(random_points)


def set_params(img, params):
    # Initialize internal params dictionary.
    _params = {
        'reducer': ee.Reducer.mean(),
        'scale': None,
        'crs': None,
        'bands': None,
        'bandsRename': None,
        'imgProps': None,
        'imgPropsRename': None,
        'datetimeName': 'datetime',
        'datetimeFormat': "YYYY-MM-dd HH:'mm':ss"
    }

    # Replace initialized params with provided params.
    if params:
        for param in params:
            _params[param] = params[param] or _params[param]

    # Set default parameters based on an image representative.
    nonSystemImgProps = ee.Feature(None) \
        .copyProperties(img).propertyNames()
    if not _params['bands']:
        _params['bands'] = img.bandNames()
    if not _params['bandsRename']:
        _params['bandsRename'] = _params['bands']
    if not _params['imgProps']:
        _params['imgProps'] = nonSystemImgProps
    if not _params['imgPropsRename']:
        _params['imgPropsRename'] = _params['imgProps']
        
    return _params


def func_ioy(img, fc, _params):
    # Subset points that intersect the given image.
    fcSub = fc.filter(ee.Filter.bounds(img.geometry()))

    # Reduce the image by regions.
    return img.reduceRegions(**{
        'collection': fcSub,
        'reducer': _params['reducer'],
        'scale': _params['scale'],
        'crs': _params['crs']
    })

#-------------------------------> Accuracy functions

def get_acc(img, params):
    fc = random_points()
    params = set_params(img, params)
    
    img_reduced = func_ioy(img, fc, params)
    results = img_reduced \
        .filter(ee.Filter.notNull(params['bandsRename']))
        
    return results