# -*- coding: utf-8 -*-
"""
@author: kuzand
"""

import numpy as np


def surface_detect_2d(img):
    '''
    Function for finding the surface of a 2D object.
    '''
    
    img = img.astype('uint8')
    img = np.pad(img, pad_width=((1, 1), (1, 1)), mode='constant')
    M, N = img.shape
    
    # Center the image
    img_centered = np.zeros((M+2, N+2), dtype=img.dtype)
    img_centered[1:-1, 1:-1] = img
    
    # Create slices for shifting the image
    slices = [(slice(1, -1), slice(2, N+2)),
              (slice(1, -1), slice(0, -2)),
              (slice(2, M+2), slice(1, -1)),
              (slice(0,-2), slice(1, -1))]
    
    # Detect the surface
    out = 0
    for s in slices:
        img_shifted = np.zeros((M+2, N+2), dtype=img.dtype)
        img_shifted[s] = img
        out |= img_centered ^ (img_centered & img_shifted)
    
    return out[2:-2, 2:-2]


def surface_detect_3d(img):
    '''
    Function for finding the surface of a 3D object.
    '''
    
    img = img.astype('uint8')

    img = np.pad(img, pad_width=((1, 1), (1, 1), (1, 1)), mode='constant')
    L, M, N = img.shape
    
    # Center the image
    img_centered = np.zeros((L+2, M+2, N+2), dtype=img.dtype)
    img_centered[1:-1, 1:-1, 1:-1] = img
    
    # Create slices for shifting the image
    slices = [(slice(1, -1), slice(1, -1), slice(2, N+2)), # shift right
              (slice(1, -1), slice(1, -1), slice(0, -2)), # shift left
              (slice(1, -1), slice(2, M+2), slice(1, -1)), # shift down
              (slice(1, -1), slice(0,-2), slice(1, -1)), # shift up
              (slice(2, L+2), slice(1, -1), slice(1, -1)), # shift front
              (slice(0, -2), slice(1, -1), slice(1, -1))] # shift back
    
    # Detect the surface
    out = 0
    for s in slices:
        img_shifted = np.zeros((L+2, M+2, N+2), dtype=img.dtype)
        img_shifted[s] = img
        out |= img_centered ^ (img_centered & img_shifted)
    
    return out[2:-2, 2:-2, 2:-2]



if __name__ == "__main__":
    
    import sys
    sys.path.append(r"../../")
    import my_utils
    
    img = my_utils.load_scans("../../../data/head256")[200]
    img_thresholded = np.zeros(img.shape, dtype=img.dtype)
    img_thresholded[img > 40] = 1
    my_utils.display_slice(img_thresholded)

    img_surface = surface_detect_2d(img_thresholded)
    my_utils.display_slice(img_surface)
    