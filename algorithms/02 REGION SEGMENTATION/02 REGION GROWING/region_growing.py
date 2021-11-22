# -*- coding: utf-8 -*-
"""
@author: kuzand
"""

import numpy as np


def region_grow_2d(img, seeds, T):
    '''
    Region growing algorithm for 2D images.
    
    Parameters
    ----------
    img: input 2D image
    seeds: blank 2D image containing the seeds (pixels with non-zero value)
    T: threshold
    '''
    output = seeds.astype('float')
    M, N = img.shape
    num_regions = (output > 0).sum()
    
    # Initialization of temporary buffers
    BR = np.zeros((M, N), dtype='uint8')  # border buffer
    XC = np.zeros((M, N), dtype='uint8')  # flag buffer
    S = np.zeros(num_regions)  # sum of the intensities of the pixels of each region
    NP = np.zeros(num_regions)  # number of points of each region
    ME = np.zeros(num_regions)  # mean intensities of each region
    
    # Use seeds to initialize BR,XC,NP,ME,S
    i = 0
    for row in range(M):
        for col in range(N):
            if output[row, col] > 0:
                i += 1
                output[row, col] = i
                BR[row, col] = i
                XC[row, col] = 1
                S[i - 1] = img[row, col]
                ME[i - 1] = img[row, col]
                NP[i - 1] += 1
                
    # Main region growing segmentation loop
    while True:
        stop = True
        for row in range(1, M-1):
            for col in range(1, N-1):
                if BR[row, col] > 0:
                    m = BR[row, col]
                    stop = False
                    for dr in range(-1, 2):
                        for dc in range(-1, 2):
                            if (XC[row + dr, col + dc] == 0 and 
                                abs(img[row + dr, col + dc] - ME[m - 1]) <= T):
                                output[row + dr, col + dc] = m
                                BR[row + dr, col + dc] = m
                                XC[row + dr, col + dc] = 1
                                NP[m - 1] += 1
                                S[m - 1] += img[row + dr, col + dc]
                    BR[row, col] = 0
        if stop:
            break
        
    # Calculate the mean values of the regions
    for i in range(num_regions):
        ME[i] = S[i] / NP[i]
            
    # Scan output image sequence and label the assigned points by
    # the mean value of the corresponding region
    for row in range(M):
        for col in range(N):
            if output[row, col] > 0:
                m = int(output[row, col])
                output[row, col] = ME[m - 1]
    
    return output


def region_grow_3d(img, seeds, T):
    '''
    Region growing algorithm for 3D images.
    
    Parameters
    ----------
    img: input 3D image
    seeds: blank 3D image containing the seeds (pixels with non-zero value)
    T: threshold
    '''
    output = seeds.astype('float')
    L, M, N = img.shape
    num_regions = (output > 0).sum()
    
    # Initialization of temporary buffers
    BR = np.zeros((L, M, N), dtype='uint8')  # border buffer
    XC = np.zeros((L, M, N), dtype='uint8')  # flag buffer
    S = np.zeros(num_regions)  # sum of the intensities of the voxels of each region
    NP = np.zeros(num_regions)  # number of points of each region
    ME = np.zeros(num_regions)  # mean intensities of each region
    
    # Use seeds to initialize BR,XC,NP,ME,S
    i = 0
    for frame in range(L):
        for row in range(M):
            for col in range(N):
                if output[frame, row, col] > 0:
                    i += 1
                    output[frame, row, col] = i
                    BR[frame, row, col] = i
                    XC[frame, row, col] = 1
                    S[i - 1] = img[frame, row, col]
                    ME[i - 1] = img[frame, row, col]
                    NP[i - 1] += 1
                
    # Main region growing segmentation loop
    while True:
        stop = True
        counter = 0
        for frame in range(L):
            for row in range(1, M-1):
                for col in range(1, N-1):
                    counter += 1
                    if counter % 10000 == 0: print(f"{counter}/{L*M*N}")
                    if BR[frame, row, col] > 0:
                        m = BR[frame, row, col]
                        stop = False
                        for df in range(-1, 2):
                            for dr in range(-1, 2):
                                for dc in range(-1, 2):
                                    if (XC[frame + df, row + dr, col + dc] == 0 and 
                                        abs(img[frame + df, row + dr, col + dc] - ME[m - 1]) <= T):
                                        output[frame + df, row + dr, col + dc] = m
                                        BR[frame + df, row + dr, col + dc] = m
                                        XC[frame + df, row + dr, col + dc] = 1
                                        NP[m - 1] += 1
                                        S[m - 1] += img[frame + df, row + dr, col + dc]
                        BR[frame, row, col] = 0
        if stop:
            break
        
    # Calculate the mean values of the regions
    for i in range(num_regions):
        ME[i] = S[i] / NP[i]
            
    # Scan output image sequence and label the assigned points by
    # the mean value of the corresponding region
    for frame in range(L):
        for row in range(M):
            for col in range(N):
                if output[row, col] > 0:
                    m = int(output[row, col])
                    output[row, col] = ME[m - 1]
    
    return output



if __name__ == "__main__": 
        
    import sys
    sys.path.append(r"../../")
    import my_utils
    
    img_2d = my_utils.load_scans("../../../data/head256")[200]
    my_utils.display_slice(img_2d)
    
    seeds = np.zeros_like(img_2d)
    seeds[57, 155] = 1

    output = region_grow_2d(img_2d, seeds, 80)
    my_utils.display_slice(output)
    
    