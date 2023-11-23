import ee
import geemap

#----------------------------> Classification

def classification(LULC_dataset):
    # This is the LULC labels
    LULC = ee.ImageCollection(LULC_dataset).mosaic()
    
    landsat8 = ee.ImageCollection('LANDSAT/LC08/C02/T1')
    l8_image = ee.Algorithms.Landsat.simpleComposite(**{
        'collection': landsat8.filterDate('2018-01-01', '2018-12-31'),
        'asFloat': True
    })
    
    image = l8_image.addBands(LULC)
    
    return image

# -------------------------> Export functions

def export_image_task(image_classified, output_folder = '/Users/gustavodanon/Downloads'):
    import os
    import time

    task_config = {
        'image': image_classified,
        'description': 'Supervised_Classification',
        'scale': 30,
        'region': Italy.geometry(),
        'fileFormat': 'GeoTIFF'
    }

    task = ee.batch.Export.image.toDrive(**task_config)

    task.start()

    while task.status()['state'] in ['READY', 'RUNNING']:
        print('Waiting on (id: {}).'.format(task.id))
        time.sleep(10)
        print(task.status())

    if task.status()['state'] == 'COMPLETED':
        import subprocess

        subprocess.call(['earthengine', 'cp', task.status()['destination_uris'][0], output_folder])

        print('File downloaded to your computer:', os.path.join(output_folder, 'image_export.tif')) # Set namme
    else:
        print('Export task failed or encountered an error.')
        

def export_table_task(table, output = 'GEE Output'):
    import os
    import time
    
    out_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
    out_csv = os.path.join(out_dir, 'table.shp')
    task_config = {
        'ee_object': table,
        'filename': out_csv,
        'timeout': float("inf")
    }
    
    geemap.ee_export_vector(**task_config)
    
    
    # task = ee.batch.Export.table.toDrive(**task_config)
    
    # task.start()

    # while task.status()['state'] in ['READY', 'RUNNING']:
    #     print('Waiting on (id: {}).'.format(task.id))
    #     time.sleep(10)
    #     print(task.status())

    # if task.status()['state'] == 'COMPLETED':
    #     print('Task Completed.')
    # else:
    #     print('Export task failed or encountered an error.')
    