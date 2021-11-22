Region splitting is a region-based image segmentation method. In contrast to the region growing algorithm, it follows a top-down approach. That is, it starts from the entire 3D image and proceeds toward voxel level through a series of successive splits.

The algorithms can be implemented in a recursive fashion as follows: Each region is checked for homogeneity and if found to be non-homogeneous it is split into eight subregions (octants). Then the splitting function is called for each of the subregions.

Homogeneity of a region can be judged by comparing the absolute difference of maximum and minimum voxel intensities within the region against a user defined threshold T:

|max⁡ - min| < T
                 
Or alternatively the local intensity variance can be used:
                 
var(x) < T

[1] Pitas I, Nikolaidis N, “3-D image processing algorithms”, Wiley (2000).
