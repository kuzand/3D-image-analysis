# -*- coding: utf-8 -*-
"""
@author: kuzand
"""

import numpy as np
from scipy import signal


def sobel_3d(img, fast=True):
    '''
    Function for 3D edge detection using 3D Sobel masks.
    '''
    L, M, N = img.shape
    output = np.zeros((L, M, N), dtype=img.dtype)
    
    sobel_x = np.array([[[-1, 0, 1],
                         [-2, 0, 2],
                         [-1, 0, 1]],
                        [[-2, 0, 2],
                         [-3, 0, 3],
                         [-2, 0, 2]],
                        [[-1, 0, 1],
                         [-2, 0, 2],
                         [-1, 0, 1]]])
    sobel_y = np.rot90(sobel_x, 1, (2, 1))
    sobel_z = np.rot90(sobel_x, 1, (2, 0))
    
    if fast == False:
        for frame in range(1, L-1):
            for row in range(1, M-1):
                for col in range(1, N-1):
                    # 3x3x3 image patch centered at (frame, row, col)
                    img_patch = img[frame-1:frame+2, row-1:row+2, col-1:col+2]
                    # L1 norm
                    k = abs(np.sum(img_patch * sobel_x)) +\
                        abs(np.sum(img_patch * sobel_y)) +\
                        abs(np.sum(img_patch * sobel_z))
                        
                    if k > img.max(): k = img.max()
                    output[frame, row, col] = k
    else:
        output = np.abs(signal.convolve(img, sobel_x, mode='valid')).astype(img.dtype)
        output += np.abs(signal.convolve(img, sobel_y, mode='valid')).astype(img.dtype)
        output += np.abs(signal.convolve(img, sobel_z, mode='valid')).astype(img.dtype)
        output[output > img.max()] = img.max()
        output = np.pad(output, pad_width=((1, 1), (1, 1), (1, 1)), mode='constant')
            
    return output



if __name__ == "__main__":
    
    import sys
    sys.path.append(r"../../")
    import my_utils
    
    img = (~my_utils.create_volume()).astype('uint8')
    out = sobel_3d(img, fast=False)
    my_utils.display_voxels(out, empty_color='#1f77b410', non_empty_color='#7A88CCC0')
    
    # img_3d = my_utils.load_scans("../../../data/head256")
    # my_utils.display_slice(img_3d[200])

    # output = sobel_3d(img_3d, fast=True)
    # my_utils.display_slice(output[200])
    