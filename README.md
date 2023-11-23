# MATSUM LULC Enrichment

## Notebook responsible for extracting data from public datasets and enriching MATSUM

### Quick Introduction

There are two methods for enriching the data: land cover enrichment and land use enrichment. Land cover enrichment involves importing pre-classified datasets from online sources and extracting the percentage of each class in regions of interest. On the other hand, land use enrichment uses the LUCAS dataset for supervised classification.

Both tasks rely on the use of the Earth Engine (EE) and geemap libraries. The folders included in this package are organized as follows:
* "main": contains the main code.
* "geemap_tests": includes some examples of geemap functions. In particular, please note the "draw_features" function which can be used to draw and extract features on the map, and the "dataset_exploration" function which is used to explore the datasets available on geemap.

Check GEEMAP API: https://geemap.org/common/ (it is very useful)

### Step-by-Step Utilization

0 - Environment

0.1 - Defining Credentials

To use the libraries, enable Earth Engine API on your Google Cloud project. You can either authenticate using "ee.Authenticate" function or create a service account private key and specify its path at the beginning of the code.

0.2 - ROIS

Define the Regions Of Interest in the "ROIs.geojson" file. The features inside the ROIS file are expected to be a FeatureCollection-like file, and its features should be polygons.

1 - Land Cover

Examples of LandCover data extraction are available. Output class codes follow dataset codification. Check references for correct mapping.

1.1 - Set Parameters

Inside each code set the parameters: 
* The path for ROIs file
* Output folder and file name

If another dataset is desired:
* Change dataset parameter value for the dataset template
* Note the band selection

2 - Land Use (LUCAS)

Lucas Link: https://esdac.jrc.ec.europa.eu/projects/lucas
I used the 2018 dataset for Italy.

2.1 - Get Training Data

Sample folders containing LUCAS training data separated by hierarchy levels are available.
In order to get other samples (or just resampling) refer to "get_training" file (I recommend running it in collab).

2.1.1 - get_training

* Change the "to_list" parameter for the desired hierarchy level and change the label column length accordingly.
* Since Earth Engine has a limitation on more than 5000 elements on some functions, filter "randomLucas" on many files as needed (i.e. change "lucas_fc" definition parameters). I did it in 3 files for each hierarchy level. Since I filtered problematic rows, I got around 14k elements for each hierarchy level.

* Change the output filename at the end. Note that the code runs a batch export task. Adapt it as needed.
  Note that the task exports the file to Google Drive. Be sure to download it and save it in sample folders.


2.2 - Supervised Classification

* Change "folder_path" if another hierarchy is desired.
* Change the "split" parameter for cross-validation (it's being used as 80/20)
* Changing the classifier: 5th code cell - trained = CLASSIFIER....
  The Classifiers are defined on the "classifier" file. Above the training step, the accuracies are shown.
  Note that the "bands" parameter refers to the fields that are utilized during the training process. Change it as needed.
* Change ROIs path and output path at the end of the code

3 - Other Parameters

To change any other specific parameters (especially inside another library function), such as scale, refer to "zonal_statistics_by_group" in the GEEMAP API. 

### Observações / To Do

# Data: 23-11-2023
# Gustavo Danon
