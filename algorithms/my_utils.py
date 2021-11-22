# -*- coding: utf-8 -*-

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.cm as cm
from skimage import io
import os
import re


def load_scans(path):
    
    files = []
    for fname in os.listdir(path):
        if fname.lower().endswith('.tif'):
            files.append(fname)
    files.sort(key=lambda f: int(re.sub('\D', '', f)))

    slices = []
    for fname in files:
        s = io.imread(os.path.join(path, fname))
        slices.append(s)
    
    img3d = np.array(slices)
    
    return img3d



def binarize(image, threshold):
    return (image >= threshold).astype('uint8')
    

def display_slice(volume_slice, title=''):
    fig, ax = plt.subplots()
    ax.imshow(volume_slice, cmap='bone')
    ax.set_title(title)
    plt.show()



def display_voxels(volume, non_empty_color='#1f77b410', empty_color='#7A88CCC0', title=''):
    """
    volume: (N,M,P) array
            Represents a binary set of pixels: objects are marked with 1,
            complementary (porosities) with 0.

    The voxels are actually represented with blue transparent surfaces.
    Inner porosities are represented in red.
    """
    
    if volume.size > 10000:
        raise Exception("volume too big to display")
    
    # Upscale the above voxel image, leaving gaps
    size = np.array(volume.shape) * 2
    
    filled = np.zeros(size-1, dtype=volume.dtype)
    filled[::2, ::2, ::2] = np.ones(volume.shape, dtype=volume.dtype)
        
    fcolors = np.zeros(size-1, dtype='<U9')
    fcolors[::2, ::2, ::2] = np.where(volume, non_empty_color, empty_color)  # '#ff0000ff'
    
    # Shrink the gaps between voxels
    x, y, z = np.indices(np.array(filled.shape) + 1)
    x[1::2, :, :] += 1
    y[:, 1::2, :] += 1
    z[:, :, 1::2] += 1
    
    # Define 3D figure and place voxels
    ax = plt.figure().add_subplot(projection='3d')
    ax.grid(False)
    ax.set_axis_off()
    ax.voxels(x, y, z, filled, facecolors=fcolors)
    ax.set_title(title)
    plt.show()
    
    
def create_volume():
    # Define a volume of 7x7x7 voxels
    n = 7
    cube = np.ones((n, n, n), dtype=bool)
    
    # Add a tunnel
    c = int(n/2)
    cube[c, :, c] = False
    
    # Add a new hole
    cube[int(3*n/4), c-1, c-1] = False
    
    # Add a hole in neighbourhood of previous one
    cube[int(3*n/4), c, c] = False
    
    # Add a second tunnel
    cube[:, c, int(3*n/4)] = False
    
    return cube


def draw_bbox_2d(img, x_min, y_min, x_max, y_max):
        
    # Create figure and axes
    fig, ax = plt.subplots()
    
    # Display the image
    ax.imshow(img, cmap='nipy_spectral')
    
    # Create a Rectangle patch
    rect = patches.Rectangle((y_min-0.5, x_min-0.5), y_max-y_min+1, x_max-x_min+1,
                             linewidth=1, edgecolor='red', facecolor='none')

    # Add the patch to the Axes
    ax.add_patch(rect)

    plt.show()




