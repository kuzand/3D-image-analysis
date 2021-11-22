# -*- coding: utf-8 -*-
"""
@author: kuzand
"""

import numpy as np


def range_3d(img, window_size):
    '''
    Function for 3D edge detection using the range operator.
    '''
    L, M, N = img.shape
    Lw, Mw, Nw = window_size
    L_1 = Lw//2
    M_1 = Mw//2
    N_1 = Nw//2
    L_2 = L - Lw//2
    M_2 = M - Mw//2
    N_2 = N - Nw//2
    
    output = np.zeros((L, M, N), dtype='uint8')
    
    for frame in range(L_1, L_2):
        for row in range(M_1, M_2):
            for col in range(N_1, N_2):
                # 3x3x3 image patch centered at (frame, row, col).
                img_patch = img[frame-1:frame+2, row-1:row+2, col-1:col+2]
                # Compute the difference between the maximum and minimum
                # intensity value within the window.
                output[frame, row, col] = img_patch.max() - img_patch.min()
            
    return output



if __name__ == "__main__":
    
    import sys
    sys.path.append(r"../../")
    import my_utils
    
    # Too slow...
    img_3d = my_utils.load_scans("../../../data/head256")
    my_utils.display_slice(img_3d[200])

    output = range_3d(img_3d, window_size=(3, 3, 3))
    my_utils.display_slice(output[200])