Region splitting is a region-based image segmentation method. In contrast to the region growing algorithm, it follows a top-down approach. That is, it starts from the entire 3D image and proceeds to voxel level through a series of successive splits.

The algorithms can be implemented in a recursive fashion. If a region of the 3D image is non-homogeneous then it is split into eight subregions (octants). The splitting into subregions is recursively applied to each of the resulted subregions until no further splitting occurs. Initially the whole 3D image is considered as one region.

Homogeneity of a region can be judged by comparing the absolute difference of maximum and minimum voxel intensities within the region against a user defined threshold T:

|max⁡ - min| < T
                 
Or alternatively the local intensity variance can be used:
                 
var(x) < T

[1] Pitas I, Nikolaidis N, “3-D image processing algorithms”, Wiley (2000).
