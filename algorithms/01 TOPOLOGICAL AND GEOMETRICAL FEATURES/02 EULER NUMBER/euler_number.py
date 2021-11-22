# -*- coding: utf-8 -*-
"""
@author: kuzand
"""

import numpy as np
from skimage.measure import euler_number


# Lookup table used for the Euler number evaluation
TABLE = np.loadtxt("table.csv", dtype='int', delimiter=",")[:, 1]


def euler_number(img):
    
    L, M, N = img.shape
    img = np.pad(img, pad_width=((1,1), (1,1), (1,1)), mode='constant')
    
    euler = 0
    for frame in range(1, L+1):
        for row in range(1, M+1):
            for col in range(1, N+1):
                if img[frame, row, col] == 1:
                    # Form the table index
                    index = (img[frame, row+1, col] |
                             img[frame, row, col+1] << 1 |
                             img[frame+1, row, col] << 2 |
                             img[frame, row+1, col+1] << 3 |
                             img[frame+1, row+1, col] << 4 |
                             img[frame+1, row, col+1] << 5 |
                             img[frame+1, row+1, col+1] << 6)
                    # Add the contribution of this voxel to the total Euler number
                    euler += TABLE[index]
    return euler



if __name__ == "__main__":
    
    import sys
    sys.path.append(r"../../")
    import my_utils
    
    img = my_utils.create_volume()
    euler_num = euler_number(img)
    my_utils.display_voxels(img, title=f'6-connectivity\ncomponents: 1, cavities:1, tunnels:2\nEuler number:{euler_num}')
    