Region growing is a region-based image segmentation method. It constructs 3D regions by starting from some voxels called seeds that are provided by the user. By placing the seeds at different locations we can specify the objects that will be segmented.

The algorithm goes as follows: At each iteration the algorithm finds the boundary voxels of the regions that participate in the growing procedure. Foe each of these voxels we check its neighborhood for voxels that are not assigned to some region and whose intensity is close to the mean intensity of the region under consideration. If both conditions are satisfied, such a voxel is assigned to this region. Each region grows until it collides with another region or reaches a different intensity area. The algorithm stops when no voxels to be classified can be found.

[1] Pitas I, Nikolaidis N, “3-D image processing algorithms”, Wiley (2000).
