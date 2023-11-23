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
    pixel_coordinates = pixel_data.get(pixel_key).getInfo()
        
    return pixel_coordinates

def compute_new_column(geom, ee_image, classes_qnt, pixel_key):
    # Convert the GeoJSON coordinates to Earth Engine Geometry
    coordinates = geom.exterior.coords if geom.exterior else None
    
    roi = ee.Geometry.Polygon(list(coordinates))
    roi_info = extract_pixel_data(ee_image.clip(roi), roi, pixel_key)
    
    classes_cnt = [0]*classes_qnt

    # Count occurrences of each value
    for value in roi_info:
        classes_cnt[value]+=1

    return str([value / len(roi_info) for value in classes_cnt])
    

def add_landcover_column(ee_image, gpd_file, classes_qnt, pixel_key='landcover', column_name = 'landcover'):
    
    gdf = gpd.read_file(gpd_file)
    
    gdf[column_name] = gdf['geometry'].apply(lambda x: compute_new_column(x, ee_image, classes_qnt, pixel_key))

    return gdf