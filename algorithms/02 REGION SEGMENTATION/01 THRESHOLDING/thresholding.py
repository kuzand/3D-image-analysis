# -*- coding: utf-8 -*-
"""
@author: kuzand
"""

import numpy as np


def threshold_3d(img, T):
    '''
    Function to threshold the input 3D image using threshold T.
    For every voxel of the image which is above the trheshold T,
    the corresponding output image voxel is given the value 1, 
    otherwise it is given the value 0.
    '''
    
    # Usingy numpy:
    # return (img >= T).astype('uint8')

    L, M, N = img.shape
    output = np.zeros((L, M, N), dtype='uint8')
    
    for frame in range(L):
        for row in range(M):
            for col in range(N):
                if img[frame, row, col] >= T:
                    output[frame, row, col] = 1
    return output



if __name__ == "__main__":
    
    import sys
    sys.path.append(r"../../")
    import my_utils
    
    img = my_utils.load_scans("../../../data/sample2_neuron")
    my_utils.display_slice(img[10])
    
    img_binary = threshold_3d(img, T=40)
    my_utils.display_slice(img_binary[10])
                    