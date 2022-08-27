"""
TWM: Tiled Web Map
"""

import math
import numpy as np

def LatLonToTileIndex(lat, lon, zoom):
    "Converts lat/lon to pixel coordinates in given zoom of the EPSG:4326 pyramid"
    lat_rad = math.radians(lat)
    n = 2.0 ** zoom
    px = int((lon + 180.0) / 360.0 * n)
    py = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return (px, py)

def tile2lon(x, z):
    return x / math.pow(2.0, z) * 360.0 - 180.0

def tile2lat( y, z):
    n = math.pi - (2.0 * math.pi * y) / math.pow(2.0, z)
    return math.degrees(math.atan(math.sinh(n)))

def TileBounds(tx, ty, zoom):
    return (
        tile2lon(tx, zoom),
        tile2lat(ty, zoom),
        tile2lon(tx + 1, zoom),
        tile2lat(ty + 1, zoom)
    )

def changeInterval(oldP, old, new):
    '''
        p0-----------+
        |            |     p0------+
        |    Old     | ==> |  New  |
        |            |     +------p1
        +-----------p1
    '''
    oldP0, oldP1 = old
    newP0, newP1 = new

    res = []
    for idx in range(2):
        oldMin, oldMax = oldP0[idx], oldP1[idx]
        newMin, newMax = newP0[idx], newP1[idx]
        oldRange = (oldMax - oldMin)
        newRange = (newMax - newMin)
        res.append(round((((oldP[idx] - oldMin) * newRange) / oldRange) + newMin))
    return res

def getIntersection(box0, box1):
    '''
              p10--------------+
               |               |
       p00-----+--------+      |
        |      |////////|      |
        |      |////////|      |
        |      +--------+-----p11
        |               |
        +--------------p01
    '''
    p00, p01 = box0
    p10, p11 = box1

    p0_x = max(p00[0], p10[0])
    p0_y = max(p00[1], p10[1])
    p1_x = min(p01[0], p11[0])
    p1_y = min(p01[1], p11[1])

    return p0_x, p0_y, p1_x, p1_y

def gray2rgba(gray, colors=None):
    '''
        x-----------x    x-----R-----x
        |           |    | x-----G---+-x
        |   gray    | => | | x-----B---+-x
        |           |    | | | x-----a---+-x
        x-----------x    x-| | |           |
                           x-| |           |
                             x-|           |
                               x-----------x
    '''
    rgba = np.stack((gray.reshape(gray.shape[1:]),)*4, axis=-1)
    alpha = rgba[:, :, 3]
    alpha[alpha != 0] = 255
    rgb = rgba[:, :, :3]

    if colors:
        for key, value in colors.items():
            rgb[np.where((rgb == int(key)).all(axis=2))] = value
    else:
        rgb[np.where((rgb != 0).all(axis=2))] = (255, 0, 0)

    rgba[:, :, 0:3] = rgb
    rgba[:, :, 3] = alpha
    return rgba

