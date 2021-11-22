# -*- coding: utf-8 -*-
"""
@author: kuzand
"""

import numpy as np



def test2d_homogeneity(img, M_1, M_2, N_1, N_2, T):
    '''
    Function to test if the given 2D image region defined by coordinates 
    M_1:M_2 and N_1:N2 is homogeneous or non-homogeneous.
    '''
    if abs(img[M_1:M_2, N_1:N_2].max() - img[M_1:M_2, N_1:N_2].min()) < T:
        return True
    else:
        return False
    
    
def test3d_homogeneity(img, L_1, L_2, M_1, M_2, N_1, N_2, T):
    '''
    Function to test if the given 3D image region defined by coordinates 
    L_1:L_2, M_1:M_2 and N_1:N2 is homogeneous or non-homogeneous.
    '''
    if abs(img[L_1:L_2, M_1:M_2, N_1:N_2].max() - img[L_1:L_2, M_1:M_2, N_1:N_2].min()) < T:
        return True
    else:
        return False
    

def region_split_2d(img, M_1, M_2, N_1, N_2, T):
    '''
    Region splitting algorithm for 2D images.
    
    Parameters
    ----------
    img: input 2D image
    T: segmentation threshold
    M_1, N_1: start coordinates (row, column)
    M_2, N_2: end coordinates (row, column)
    '''
    
    if M_2 - M_1 == N_2 - N_1 == 1:
        return img[M_1:M_2, N_1:N_2]
    
    output_img = np.zeros((M_2 - M_1, N_2 - N_1), dtype=img.dtype)

    # Flags to show if splitting in the corresponding dimension can continue
    M_continue = True
    N_continue = True
    
    # Check if the input region is homogeneous
    is_homogeneous = test2d_homogeneity(img, M_1, M_2, N_1, N_2, T)
    
    # If it is not homogeneous, split it in four regions
    if (is_homogeneous == False) and (M_2 - M_1 > 1 or N_2 - N_1 > 1):
        if M_2 - M_1 == 1:
            M_half = M_2
            M_continue = False
        else:
            M_half = M_1 + (M_2 - M_1)//2
            
        if N_2 - N_1 == 1:
            N_half = N_2
            N_continue = False
        else:
            N_half = N_1 + (N_2 - N_1)//2

        output_img[0:M_half-M_1, 0:N_half-N_1] = region_split_2d(img, M_1, M_half, N_1, N_half, T)  # first quadrant
        if N_continue:
            output_img[0:M_half-M_1, N_half-N_1:N_2-N_1] = region_split_2d(img, M_1, M_half, N_half, N_2, T)  # second quadrant
        if M_continue:
            output_img[M_half-M_1:M_2-M_1, 0:N_half-N_1] = region_split_2d(img, M_half, M_2, N_1, N_half, T)  # third quadrant
        if M_continue and N_continue:
            output_img[M_half-M_1:M_2-M_1, N_half-N_1:N_2-N_1] = region_split_2d(img, M_half, M_2, N_half, N_2, T)  # fourth quadrant
            
    # If the region is homogeneous, calculate its mean intensity and assign
    # it to all the points of this region in the output image   
    elif is_homogeneous == True:
        output_img[:, :] = np.mean(img[M_1:M_2, N_1:N_2])
        
    return output_img


def region_split_3d(img, L_1, L_2, M_1, M_2, N_1, N_2, T):
    '''
    Region splitting algorithm for 3D images.
    
    Parameters
    ----------
    img: input 3D image
    T: segmentation threshold
    L_1, M_1, N_1: start coordinates (frame, row, column)
    L_2, M_2, N_2: end coordinates (frame, row, column)
    '''
    
    if L_2 - L_1 == M_2 - M_1 == N_2 - N_1 == 1:
        return img[L_1:L_2, M_1:M_2, N_1:N_2]
    
    output_img = np.zeros((L_2 - L_1, M_2 - M_1, N_2 - N_1), dtype=img.dtype)

    # Flags to show if splitting in the corresponding dimension can continue
    L_continue = True
    M_continue = True
    N_continue = True
    
    # Check if the input region is homogeneous
    is_homogeneous = test3d_homogeneity(img, L_1, L_2, M_1, M_2, N_1, N_2, T)
    
    # If it is not homogeneous, split it in eight regions
    if (is_homogeneous == False) and (L_2 - L_1 > 1 or M_2 - M_1 > 1 or N_2 - N_1 > 1):
        
        if L_2 - L_1 == 1:
            L_half = L_2
            L_continue = False
        else:
            L_half = L_1 + (L_2 - L_1)//2
        
        if M_2 - M_1 == 1:
            M_half = M_2
            M_continue = False
        else:
            M_half = M_1 + (M_2 - M_1)//2
            
        if N_2 - N_1 == 1:
            N_half = N_2
            N_continue = False
        else:
            N_half = N_1 + (N_2 - N_1)//2

        output_img[0:L_half-L_1, 0:M_half-M_1, 0:N_half-N_1] = region_split_3d(img, L_1, L_half, M_1, M_half, N_1, N_half, T)
        if M_continue:
            output_img[0:L_half-L_1, M_half-M_1:M_2-M_1, 0:N_half-N_1] = region_split_3d(img, L_1, L_half, M_half, M_2, N_1, N_half, T)        
        if N_continue:
            output_img[0:L_half-L_1, 0:M_half-M_1, N_half-N_1:N_2-N_1] = region_split_3d(img, L_1, L_half, M_1, M_half, N_half, N_2, T)
        if M_continue and N_continue:
            output_img[0:L_half-L_1, M_half-M_1:M_2-M_1, N_half-N_1:N_2-N_1] = region_split_3d(img, L_1, L_half, M_half, M_2, N_half, N_2, T)
        if L_continue:
            output_img[L_half-L_1:L_2-L_1, 0:M_half-M_1, 0:N_half-N_1] = region_split_3d(img, L_half, L_2, M_1, M_half, N_1, N_half, T)
        if L_continue and M_continue:
            output_img[L_half-L_1:L_2-L_1, M_half-M_1:M_2-M_1, 0:N_half-N_1] = region_split_3d(img, L_half, L_2, M_half, M_2, N_1, N_half, T)            
        if L_continue and N_continue:
            output_img[L_half-L_1:L_2-L_1, 0:M_half-M_1, N_half-N_1:N_2-N_1] = region_split_3d(img, L_half, L_2, M_1, M_half, N_half, N_2, T)            
        if L_continue and M_continue and N_continue:
            output_img[L_half-L_1:L_2-L_1, M_half-M_1:M_2-M_1, N_half-N_1:N_2-N_1] = region_split_3d(img, L_half, L_2, M_half, M_2, N_half, N_2, T)            
   
    # If the region is homogeneous, calculate its mean intensity and assign
    # it to all the points of this region in the output image
    elif is_homogeneous == True:
        output_img[:, :, :] = np.mean(img[L_1:L_2, M_1:M_2, N_1:N_2])
        
    return output_img



if __name__ == "__main__": 
       
    import sys
    sys.path.append(r"../../")
    import my_utils
    
    # # 2D
    img_2d = my_utils.load_scans("../../../data/head256")[200]
    my_utils.display_slice(img_2d)

    output_img_2d = region_split_2d(img_2d, 0, img_2d.shape[0], 0, img_2d.shape[1], T=60)
    my_utils.display_slice(output_img_2d)
    
    # 3D (too slow...)
    # img_3d = my_utils.load_scans("../../../data/head256")
    # my_utils.display_slice(img_3d[200])

    # output_img_3d = region_split_3d(img_3d, 0, img_3d.shape[0], 0, img_3d.shape[1], 0, img_3d.shape[2], T=60)
    # my_utils.display_slice(output_img_3d[200])