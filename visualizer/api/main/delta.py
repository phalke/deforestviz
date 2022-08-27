#!/usr/bin/env python3

from datetime import date

class Delta():
    """
    process the tiff file to filter out the data outside the given date range.
    """
    def __init__(self, image, alert=None):
        self.image = image
        self.alert = alert

    @classmethod
    def dateMapping(cls, _date):
        '''Compute the number of days since 1/1/2019'''
        initDate = date(2019, 1, 1)
        return (_date - initDate).days

    def diff(self, start, end):
        '''Filter out the values outside the range [start, end]'''
        start = self.dateMapping(start) # number of days from 1/1/2019 to start
        end = self.dateMapping(end) # number of days from 1/1/2019 to end

        try:
            # Filter data
            lower = self.image<start
            upper = self.image>end
            self.image[lower] = 0
            self.image[upper] = 0
            if self.alert:
                self.alert[lower] = 0
                self.alert[upper] = 0
        except:
            pass

        return self.image, self.alert


# Test
if __name__ == '__main__':
    import rasterio as rio
    import numpy as np
    import matplotlib.pyplot as plt
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--tiff', help='Path to the .tiff file', required=True)
    args = vars(parser.parse_args())

    # filename = './S2alert_alertDate_080W_10N_070W_20N.tiff'
    filename = args['tiff']
    with rio.open(filename, 'r') as tiff:
        crs = tiff.crs
        transform = tiff.transform
        width, height = tiff.width, tiff.height
        window = rio.windows.Window(width - 10500, height - 5000, 3000, 3500)
        # extract a relatively small window from the original large tiff file.
        band = tiff.read(1, window=window).astype(np.float32)

    delta = Delta(band)
    d = delta.diff(start=date(2022, 3, 1), end=date(2022, 7, 1))

    # Display result
    plt.imshow(d, cmap='gray')
    plt.show()
