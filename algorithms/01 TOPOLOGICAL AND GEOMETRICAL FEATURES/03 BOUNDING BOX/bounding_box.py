# -*- coding: utf-8 -*-
"""
@author: kuzand
"""

import numpy as np


def bbox_2d(img, label=1):
    '''
    Function to find (axis-aligned) bounding box of the input 2D object.
    
    Returns the coordinates of two points that define the bounding box:
    (row_min, col_min) and (row_max, col_max)
    '''
    
    M, N = img.shape
    
    x_min, y_min = -1, -1
    x_max, y_max = -1, -1
    
    # Find x_min
    loop_flag = True
    x = 0
    while x < M and loop_flag == True:
        y = 0
        while y < N and loop_flag == True:
            if img[x, y] == label:
                x_min = x
                loop_flag = False
            y += 1
        x += 1
        
    # Find x_max
    loop_flag = True
    x = M - 1
    while x >= 0 and loop_flag == True:
        y = 0
        while y < N and loop_flag == True:
            if img[x, y] == label:
                x_max = x
                loop_flag = False
            y += 1
        x -= 1
                
    # Find y_min
    loop_flag = True
    y = 0
    while y < N and loop_flag == True:
        x = 0
        while x < M and loop_flag == True:
            if img[x, y] == label:
                y_min = y
                loop_flag = False
            x += 1
        y += 1
    
    # Find y_max
    loop_flag = True
    y = N - 1
    while y >= 0 and loop_flag == True:
        x = 0
        while x < M and loop_flag == True:
            if img[x, y] == label:
                y_max = y
                loop_flag = False
            x += 1
        y -= 1
        
    return x_min, y_min, x_max, y_max





def bbox_3d(img, label=1):
    '''
    Function to find (axis-aligned) bounding box of the input 3D object.
    
    Returns the coordinates of two points that define the bounding box:
    (frame_min, row_min, col_min) and (frame_max, row_max, col_max)
    '''
    L, M, N = img.shape
    
    frame_min, row_min, col_min = -1, -1, -1
    frame_max, row_max, col_max = -1, -1, -1
    
    # Find row_min
    loop_flag = True
    row = 0
    while row < M and loop_flag == True:
        col = 0
        while col < N and loop_flag == True:
            frame = 0
            while frame < L and loop_flag == True:
                if img[frame, row, col] == label:
                    row_min = row
                    loop_flag = False
                frame += 1
            col += 1
        row += 1
        
    # Find row_max
    loop_flag = True
    row = M - 1
    while row >= 0 and loop_flag == True:
        col = 0
        while col < N and loop_flag == True:
            frame = 0
            while frame < L and loop_flag == True:
                if img[frame, row, col] == label:
                    row_max = row
                    loop_flag = False
                frame += 1
            col += 1
        row -= 1
    
    # Find col_min
    loop_flag = True
    col = 0
    while col < N and loop_flag == True:
        row = 0
        while row < M and loop_flag == True:
            frame = 0
            while frame < L and loop_flag == True:
                if img[frame, row, col] == label:
                    col_min = col
                    loop_flag = False
                frame += 1
            row += 1
        col += 1

    # Find col_max
    loop_flag = True
    col = N - 1
    while col >= 0 and loop_flag == True:
        row = 0
        while row < M and loop_flag == True:
            frame = 0
            while frame < L and loop_flag == True:
                if img[frame, row, col] == label:
                    col_max = col
                    loop_flag = False
                frame += 1
            row += 1
        col -= 1

    # Find frame_min
    loop_flag = True
    frame = 0
    while frame < L and loop_flag == True:
        row = 0
        while row < M and loop_flag == True:
            col = 0
            while col < N and loop_flag == True:
                if img[frame, row, col] == label:
                    frame_min = frame
                    loop_flag = False
                col += 1
            row += 1
        frame += 1

    # Find frame_max
    loop_flag = True
    frame = L - 1
    while frame >= 0 and loop_flag == True:
        row = 0
        while row < M and loop_flag == True:
            col = 0
            while col < N and loop_flag == True:
                if img[frame, row, col] == label:
                    frame_max = frame
                    loop_flag = False
                col += 1
            row += 1
        frame -= 1

    return frame_min, row_min, col_min, frame_max, row_max, col_max



if __name__ == "__main__":
    
    import sys
    sys.path.append(r"../../")
    import my_utils
    
    img = my_utils.load_scans("../../../data/head256")[200]
    img_thresholded = np.zeros(img.shape, dtype=img.dtype)
    img_thresholded[img > 40] = 1
    my_utils.display_slice(img_thresholded)
    
    x_min, y_min, x_max, y_max = bbox_2d(img_thresholded)
    my_utils.draw_bbox_2d(img_thresholded, x_min, y_min, x_max, y_max)