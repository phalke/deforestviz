from django.shortcuts import render
from django.http import HttpResponse

from datetime import date
import cv2
import numpy as np

from .delta import Delta

def gray2rgba(gray, alert=None):
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

    # duplicate the input gray to create a 4 channel image
    rgba = np.stack((gray.reshape(gray.shape),)*4, axis=-1)

    # process alpha(opacity) channel
    alpha = rgba[:, :, 3]
    alpha[alpha != 0] = 255 # set opacity to 1 for all non zero gray value
    # set opacity to 0 for all alert == 1(confidence == 1)
    alpha[alert == 1] = 0

    #process rgb channels
    rgb = rgba[:, :, :3]
    # set color according to the alert confidence level
    rgb[alert == 2, :] = (139,69,19)
    rgb[alert == 3, :] = (176,196,222)
    rgb[alert == 4, :] = (0, 0, 255)

    # rebuilt the 4 channel image
    rgba[:, :, 0:3] = rgb
    rgba[:, :, 3] = alpha
    return rgba

def home(request):
    '''Render the visualizer home view'''
    return render(request, 'main/index.html')


def tile(request, z, x, y):
    '''
        Process the tile request and return the gernerated png image
        INPUTS:
            request: object contains information about the request, params...
            z: Zoom level
            x: tile x coordinate
            y: tile y coordinate
    '''

    # extract params from request
    start = request.GET.get('start', None)
    end = request.GET.get('end', None)
    try:
        # Load alert and alertDate tiles
        alertDateFileName = f'images/alertDate/{z}/{x}/{y}.npy'
        alertFileName = f'images/alert/{z}/{x}/{y}.npy'
        alertDateImg = np.load(alertDateFileName)[:, :, 0]
        alertImg = np.load(alertFileName)[:, :, 0]

        # Compute the delta between start and end dates
        if start and end:
            # parse start and end to lists of integers
            start = start.split('-')
            start = [int(s) for s in start]
            end = end.split('-')
            end = [int(e) for e in end]
            # compute the delta
            delta = Delta(alertDateImg, alertImg)
            alertDateImg, alertImg = delta.diff(start=date(*start), end=date(*end))

        # generate the color 4 channel image
        alertDateImg = gray2rgba(alertDateImg, alertImg)
        _, png = cv2.imencode('.png', alertDateImg)
        png = png.tobytes()
        return HttpResponse(png, content_type='image/png')
    except Exception as e:
        print(e)
        return HttpResponse()
