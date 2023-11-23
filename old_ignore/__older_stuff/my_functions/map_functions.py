print("Map Imported")

import geemap
import ee

def create_map(image_classified):
    Map = geemap.Map(center=[43.710418, 10.396636], zoom=7)
    pallete = ['#24b9eb', '#12c45f', '#737875', '#9eb431']

    Map.addLayer(**{
        'ee_object': image_classified,
        'vis_params': {
            'min': 0,
            'max': 3,
            'palette': pallete
        },
        'name': 'Classified Image'
        })
    
    return Map

# ---------------------> Old Code

# roi = ee.Geometry.Rectangle(43.8, 10.5, 43.9, 10.6)

# rgb_img = geemap.ee_to_numpy(image_classified, region=Italy, default_value=-1)
# print(rgb_img.shape)
# print(rgb_img)