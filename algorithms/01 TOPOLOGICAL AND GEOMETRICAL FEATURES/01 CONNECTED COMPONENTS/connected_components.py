# -*- coding: utf-8 -*-
"""
@author: kuzand
"""

import numpy as np
from collections import deque



def label_3d(image, connectivity, min_volume=1):
    '''
    Connected component labeling, counting and volume evaluation.
    
    Input:
    ------
        image: 3D binary image of size (L, M, N)
        connectivity: int, connectivity of the foreground components (possible values: 6, 18, 26)
        min_volume: int, minimum volume of connected component to keep
    
    Output:
    -------
        labeled_array: array of size (L, M, N) with labeled connected components
        ncomponents: int, number of connected components
        volumes: list, volumes of connected components
    '''
    
    assert image.ndim == 3, "the image should be 3D"
    assert ((image==0) | (image==1)).all(), "the image should be binary"
    assert (connectivity in [6, 18, 26]), "the connectivity can be 6, 18 or 26"
    
    img = image.copy()
    L, M, N = img.shape
    labeled_array = np.zeros((L, M, N), dtype=int)
    queue = deque([])
    volumes = []  # volumes of the connected components
    ncomponents = 0
    label = 1
    for frame in range(L):
        for row in range(M):
            for col in range(N):      
                if img[frame, row, col] == 1:
                    queue.append((frame, row, col))
                    img[frame, row, col] = 0
                    labeled_array[frame, row, col] = label
                
                    volume = 0
                    while len(queue) > 0:
                        i, j, k = queue.pop()
                        for i_n, j_n, k_n in neighbouring_inds(i, j, k, L, M, N, connectivity):
                            if img[i_n, j_n, k_n] == 1:
                                img[i_n, j_n, k_n] = 0
                                labeled_array[i_n, j_n, k_n] = label
                                queue.append((i_n, j_n, k_n))
                        volume += 1
                    
                    if volume >= min_volume:
                        volumes.append(volume)
                        ncomponents += 1
                        label += 1
                    else:
                        img[frame, row, col] = 1
                        labeled_array[labeled_array == label] = 0

    return labeled_array, ncomponents, volumes



def neighbouring_inds(frame, row, col, L, M, N, connectivity):
    '''
    Function to find the indices of neighbouring voxels of a given voxel at
    (frame, row, col) for the given connectivity.
    
    '''
    # Maximum number of coordinates in which two neighbouring voxels can differ
    # for the given connectivity    
    if connectivity == 6:
        max_diff = 1
    elif connectivity == 18:
        max_diff = 2
    elif connectivity == 26:
        max_diff = 3
    
    inds = []
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            for k in [-1, 0, 1]:
                if abs(i) + abs(j) + abs(k) <= max_diff:
                    frame_n = frame + i
                    row_n = row + j
                    col_n = col + k
                    # Check if the neighbouring indices frame_n, row_n, col_n
                    # are within the limits of the image L, M, N, respectively.
                    if (frame_n >= 0 and frame_n < L and 
                            row_n >= 0 and row_n < M and 
                                col_n >= 0 and col_n < N):
                        
                        inds.append((frame_n, row_n, col_n))
    
    return inds
    


if __name__ == "__main__":
       
    import sys
    sys.path.append(r"../../")
    import my_utils

    
    img = ~my_utils.create_volume()
    
    labeled_array, ncomponents, volumes = label_3d(img, connectivity=6)
    my_utils.display_voxels(img, empty_color='#1f77b410', non_empty_color='#7A88CCC0',
                            title=f"6-connectivity\nNum. of components: {ncomponents}")
    
    labeled_array, ncomponents, volumes = label_3d(img, connectivity=26)
    my_utils.display_voxels(img, empty_color='#1f77b410', non_empty_color='#7A88CCC0',
                        title=f"26-connectivity\nNum. of components: {ncomponents}")

    