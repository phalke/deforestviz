#!/usr/bin/env python

'''
Takes the tiff files folder path as the input, outputs map tiles at the .npy format ready
to pre-processed and served at the realtime.

ARGS:
    alert_path          alert folder path.
    alertDate_path      alertDate folder path.
    max_zoom            the max zoom level to generate. The script will generate zooms
                        from 0 to max_zoom.

DETAILS:
    Resulting tiles are 256px square, regardless of the size of the source image. The
    number of tiles wide/high is determined by the 'zoom level', which is 2^zoom. In
    other words, a zoom level of 3 = 8 tiles, each resized to 256 pixels square.
For a clear explanation:
    https://www.youtube.com/watch?v=ufygsABmg8E

file structure:
    output/{input folder name}/zoom_level/x/y.png
'''

import numpy as np
import rasterio as rio
from rasterio.enums import Resampling
from tools import changeInterval, getIntersection, LatLonToTileIndex, TileBounds
import os

# Parse args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--alert_path', help='Path to the alert folder', required=True)
parser.add_argument('--alertDate_path', help='Path to the alertDate folder', required=True)
parser.add_argument('--max_zoom', help='Maximum zoom level to generete', required=True)
args = vars(parser.parse_args())
try:
    # parse max_zoom arg to int
    zoomlevel = int(args['max_zoom'])
except Exception as e:
    raise Exception(e)

dirs = [args['alert_path'], args['alertDate_path']]
for filesDir in dirs:
    filesNames = os.listdir(filesDir)
    for i, fileName in enumerate(filesNames):
        tiff_file = f'{filesDir}/{fileName}'
        with rio.open(tiff_file, 'r') as dataset:
            lat, lon, latmax, lonmax = dataset.bounds.left, dataset.bounds.bottom, dataset.bounds.right, dataset.bounds.top
            for tz in range(zoomlevel+1):
                print(f"{i+1}/{len(filesNames)} - zoom:{tz}")
                t0x, t0y = LatLonToTileIndex(lon, lat, tz)
                t1x, t1y = LatLonToTileIndex(lonmax, latmax, tz)
                tminx, tminy = min(t0x, t1x), min(t0y, t1y)
                tmaxx, tmaxy = max(t0x, t1x), max(t0y, t1y)
                for ty in range(tminy, tmaxy+1):
                    for tx in range(tminx, tmaxx+1):
                        # Get current tile boundary latlon coordinates
                        wgsbounds = TileBounds(tx, ty, tz)

                        # Get the current tile boundary XY coordinate
                        p0 = dataset.index(*wgsbounds[:2])
                        p1 = dataset.index(*wgsbounds[2:])

                        # Compute max and min XY coordinates
                        minX, maxX = min(p0[0], p1[0]), max(p0[0], p1[0])
                        minY, maxY = min(p0[1], p1[1]), max(p0[1], p1[1])

                        # Map the XY coordinates to the range 0-255
                        p0_x, p0_y = changeInterval(
                            (0, 0),
                            ((minX, minY), (maxX, maxY)),
                            ((0, 0), (255, 255))
                        )
                        p1_x, p1_y = changeInterval(
                            (dataset.height, dataset.width),
                            ((minX, minY), (maxX, maxY)),
                            ((0, 0), (255, 255))
                        )

                        '''
                        Find the intersection of data and the tile and map it the area [p0, p1]
                        '''
                        # the box coordinate to crop from the original dataset
                        w0_x, w0_y, w1_x, w1_y = getIntersection(
                            ((minX, minY), (maxX, maxY)),
                            ((0, 0), (dataset.height, dataset.width))
                        )
                        # the target box coordinates where to map the cropped box.
                        p0_x, p0_y, p1_x, p1_y = getIntersection(
                            ((p0_x, p0_y), (p1_x, p1_y)),
                            ((0, 0), (255, 255))
                        )

		                # Load data from file
                        data = dataset.read(
                            window=((w0_x,w1_x), (w0_y, w1_y)),
                            out_shape=(p1_x - p0_x, p1_y - p0_y),
                            resampling=Resampling.nearest
                        )

                        # Skip if the extracted tile does not contains any information
                        if np.all(data==0):
                            continue

                        # Create taget folder if not exist
                        folderPath = f'./output/{filesDir.split("/")[-1]}/{tz}/{tx}/'
                        try:
                            os.makedirs(folderPath)
                        except Exception as e:
                            pass

                        # Project the data into the tile image
                        filePath = f'{folderPath}{ty}'
                        if not os.path.exists(f'{filePath}.npy'):
                            # Create empty tile image
                            tile = np.zeros((256, 256, 1), dtype=np.uint64)
                        else:
                            tile = np.load(f'{filePath}.npy')

                        tile[p0_x:p1_x, p0_y: p1_y, :] =  data.reshape((data.shape[1], data.shape[2], data.shape[0]))
                        np.save(filePath, tile)
