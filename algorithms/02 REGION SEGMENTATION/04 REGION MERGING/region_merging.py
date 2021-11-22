# -*- coding: utf-8 -*-
"""
@author: kuzand
"""

import numpy as np


def region_merge_2d(img, reg_max, T):
    '''
    Region growing algorithm for 2D images.
    
    Parameters
    ----------
    img: input 2D image
    reg_max: maximum number of regions
    T: threshold
    '''
    M, N = img.shape

    # Initializations
    output = np.zeros((M, N), dtype=img.dtype)
    XC = np.zeros((M, N), dtype='uint8')  # flag buffer
    S = np.zeros(reg_max)  # sum of the intensities of the pixels of each region
    NP = np.zeros(reg_max)  # number of points of each region
    ME = np.zeros(reg_max)  # mean intensities of each region
    
    # Main loop
    nubs = 1  # number of found regions
    for row in range(M):
        for col in range(N):
            if row == 0 and col == 0:
                XC[row, col] = 1
                output[row, col] = nubs
                NP[nubs - 1] = 1
                S[nubs - 1] = img[row, col]
                ME[nubs - 1] = img[row, col]
            else:
                # For the rest of the pixels, we test if the current pixel can be
                # merged with any region in its neighborhood. Merging is allowed
                # if the pixel intensity is close to region mean intensity.
                # If more than one merges are possible, the region with the
                # closest mean intensity is chosen.
                merge = False
                dmin = 256  # minimum intensity diference with neighboring regions
                reg_num = 1  # number of the region with which current pixel is merged
                # We check the four nearest neighbors (preceeding the current pixel)
                if row == 0:
                    dr_start = 0
                else:
                    dr_start = -1
                for dr in range(dr_start, 1):
                    for dc in range(-1, 2):
                        if ((dr or dc) and (dr or dc != 1) and
                            (row + dr >= 0) and (row + dr < M) and
                            (col + dc >= 0) and (col + dc < N)):
                            if XC[row + dr, col + dc]:
                                c = abs(img[row, col] - ME[XC[row + dr, col + dc] - 1])
                                if c <= T:
                                    merge = True
                                    if c < dmin:
                                        dmin = c
                                        reg_num = XC[row + dr, col + dc]
                if merge == True:
                    XC[row, col] = reg_num
                    output[row, col] = reg_num
                    NP[reg_num - 1] += 1
                    S[reg_num - 1] += img[row, col]
                    ME[reg_num - 1] = S[reg_num - 1] / NP[reg_num - 1]
                else:
                    # If merge is not allowed with the immediately neighboring
                    # regions, try to merge it with any other possible region.
                    dmin = 256
                    for m in range(1, nubs):
                        # more than one regions may satisfy the (c<T)
                        # the region with the lowest intensity dierence is chosen
                        c = abs(img[row, col] - ME[m - 1])
                        if c <= T:
                            merge = True
                            if c < dmin:
                                dmin = c
                                reg_num = m
                    if merge == True:
                        XC[row, col] = reg_num
                        output[row, col] = reg_num
                        NP[reg_num - 1] += 1
                        S[reg_num - 1] += img[row, col]
                        ME[reg_num - 1] = S[reg_num - 1] / NP[reg_num - 1] 
                    else:
                        # If no merge is allowed create a new region
                        if nubs < reg_max:
                            nubs += 1
                            print(nubs)
                            XC[row, col] = nubs
                            output[row, col] = nubs
                            NP[nubs - 1] = 1
                            S[nubs - 1] = img[row, col]
                            ME[nubs - 1] = img[row, col]
                        
    # Scan output image sequence and label the assigned points by the
    # mean value of the corresponding region
    for row in range(M):
        for col in range(N):
            reg_num = output[row, col]
            if reg_num:
                output[row, col] = ME[reg_num - 1]
                
    return output, nubs



def region_merge_3d(img, reg_max, T):
    '''
    Region growing algorithm for 3D images.
    
    Parameters
    ----------
    img: input 3D image
    reg_max: maximum number of regions
    T: threshold
    '''
    L, M, N = img.shape

    # Initializations
    output = np.zeros((L, M, N), dtype=img.dtype)
    XC = np.zeros((L, M, N), dtype='uint8')  # flag buffer
    S = np.zeros(reg_max)  # sum of the intensities of the voxels of each region
    NP = np.zeros(reg_max)  # number of points of each region
    ME = np.zeros(reg_max)  # mean intensities of each region
    
    # Main loop
    nubs = 1  # number of found regions
    count = 0
    for frame in range(L):
        for row in range(M):
            for col in range(N):
                count += 1
                if count % 100000 == 0: print(f"{count}/{L*M*N}")
                if frame == 0 and row == 0 and col == 0:
                    XC[frame, row, col] = 1
                    output[frame, row, col] = nubs
                    NP[nubs - 1] = 1
                    S[nubs - 1] = img[frame, row, col]
                    ME[nubs - 1] = img[frame, row, col]
                else:
                    # For the rest of the voxels, we test if the current voxel can be
                    # merged with any region in its neighborhood. Merging is allowed
                    # if the voxel intensity is close to region mean intensity.
                    # If more than one merges are possible, the region with the
                    # closest mean intensity is chosen.
                    merge = False
                    dmin = 256  # minimum intensity diference with neighboring regions
                    reg_num = 1  # number of the region with which current voxel is merged
                    # We check the four nearest neighbors (preceeding the current voxel)
                    if frame == 0:
                        df_start = 0
                    else:
                        df_start = -1
                    for df in range(df_start, 1):
                        for dr in range(-1, -df + 1):
                            for dc in range(-1, 2):
                                if ((df or dr or dc) and (df or dr or dc != 1) and
                                    (row + dr >= 0) and (row + dr < M) and
                                    (col + dc >= 0) and (col + dc < N)):
                                    if XC[frame + df, row + dr, col + dc]:
                                        c = abs(img[frame, row, col] - ME[XC[frame + df, row + dr, col + dc] - 1])
                                        if c <= T:
                                            merge = True
                                            if c < dmin:
                                                dmin = c
                                                reg_num = XC[frame + df, row + dr, col + dc]
                    if merge == True:
                        XC[frame, row, col] = reg_num
                        output[frame, row, col] = reg_num
                        NP[reg_num - 1] += 1
                        S[reg_num - 1] += img[frame, row, col]
                        ME[reg_num - 1] = S[reg_num - 1] / NP[reg_num - 1]
                    else:
                        # If merge is not allowed with the immediately neighboring
                        # regions, try to merge it with any other possible region.
                        dmin = 256
                        for m in range(1, nubs):
                            # more than one regions may satisfy the (c<T)
                            # the region with the lowest intensity dierence is chosen
                            c = abs(img[frame, row, col] - ME[m - 1])
                            if c <= T:
                                merge = True
                                if c < dmin:
                                    dmin = c
                                    reg_num = m
                        if merge == True:
                            XC[frame, row, col] = reg_num
                            output[frame, row, col] = reg_num
                            NP[reg_num - 1] += 1
                            S[reg_num - 1] += img[frame, row, col]
                            ME[reg_num - 1] = S[reg_num - 1] / NP[reg_num - 1] 
                        else:
                            # If no merge is allowed create a new region
                            if nubs < reg_max:
                                nubs += 1
                                print(nubs)
                                XC[frame, row, col] = nubs
                                output[frame, row, col] = nubs
                                NP[nubs - 1] = 1
                                S[nubs - 1] = img[frame, row, col]
                                ME[nubs - 1] = img[frame, row, col]
                        
    # Scan output image sequence and label the assigned points by the
    # mean value of the corresponding region
    for frame in range (L):
        for row in range(M):
            for col in range(N):
                reg_num = output[frame, row, col]
                if reg_num:
                    output[frame, row, col] = ME[reg_num - 1]
                
    return output, nubs



if __name__ == "__main__": 
    
    import sys
    sys.path.append(r"../../")
    import my_utils
    
    # # 2D
    img_2d = my_utils.load_scans("../../../data/head256")[200]
    my_utils.display_slice(img_2d)

    output_img_2d, nubs = region_merge_2d(img_2d, 10, T=100)
    my_utils.display_slice(output_img_2d)
    
    # 3D
    # img_3d = my_utils.load_scans("../../../../../data/head256")
    # my_utils.display_slice(img_3d[200])

    # output_img_3d, nubs = region_merge_3d(img_3d, 10, T=100)
    # my_utils.display_slice(output_img_3d[200])
    
    