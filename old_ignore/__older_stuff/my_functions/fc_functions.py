print("Feature Collections Imported")

import ee
from itertools import groupby

def sort_classes(ee_feature_collection, key):
  
  sorted_collection = ee_feature_collection.getInfo()['features']
  grouped_data = {key: list(group) for key, group in groupby(sorted_collection, key=lambda x: x['properties'][key])}
  
  return grouped_data

def get_class_qntd(ee_feature_collection, key='label'):
  return len(sort_classes(ee_feature_collection, key))

def print_class_elements(ee_feature_collection, key='label'):
    grouped_data = sort_classes(ee_feature_collection, key)
    pallete = []

    # Print the grouped data
    for label, group in grouped_data.items():
        pallete.append(group[0]['properties']['color'])
        print(f"Label: {label} | Color: {group[0]['properties']['color']}")
        # for item in group:
        #     print(item)
        print(f"Number of elements: {len(group)}")