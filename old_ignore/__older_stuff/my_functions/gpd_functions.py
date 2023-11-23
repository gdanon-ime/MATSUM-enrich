import ee
import geopandas as gpd

def extract_pixel_data(image_classified, roi, pixel_key):
    pixel_data = image_classified.reduceRegion(
        reducer=ee.Reducer.toList(),
        geometry=roi,
        scale=10,
        maxPixels=1e16  # Adjust as needed
    )

    # Extract pixel coordinates and classification values
    pixel_coordinates = ee.List(pixel_data.get(pixel_key)).getInfo()

    # Print the sampled pixel coordinates and classification values
    # print(len(pixel_coordinates))
    # for i, classification in enumerate(pixel_coordinates):
    #     print(f"Pixel {i + 1} - Classification Value: {classification}")
        
    return pixel_coordinates

def compute_new_column(geom, ee_image, feature_qnt, pixel_key):
    # Convert the GeoJSON coordinates to Earth Engine Geometry
    coordinates = geom.exterior.coords if geom.exterior else None
    
    roi = ee.Geometry.Polygon(list(coordinates))
    roi_info = extract_pixel_data(ee_image, roi, pixel_key)
    
    classes_cnt = [0]*feature_qnt

    # Count occurrences of each value
    for value in roi_info:
        classes_cnt[value]+=1

    return str([value / len(roi_info) for value in classes_cnt])
    

def add_landcover_column(ee_image, gpd_file, feature_qnt, pixel_key='classification'):
    
    gdf = gpd.read_file(gpd_file)
    
    gdf['landcover'] = gdf['geometry'].apply(lambda x: compute_new_column(x, ee_image, feature_qnt, pixel_key))

    return gdf