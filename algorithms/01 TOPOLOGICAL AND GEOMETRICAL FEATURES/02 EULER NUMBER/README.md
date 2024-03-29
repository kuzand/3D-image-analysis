A 3D object can be topologically characterized by means of its cavities and tunnels. A cavity is a background component that is adjacent to and totally enclosed by a foreground component. The notion of a tunnel is more difficult to describe, since a tunnel is not a new background component and cannot be distinguished from the background. We can say that an object contains no tunnels if every closed curve in the object can be continuously deformed, within the object, to a single point.

An important topological characteristic that combines the notion of components, cavities and tunnels is the Euler characteristic (or Euler number). The Euler characteristic χ(S) of a 3D object S is defined as follows:

χ(S) = (components) - (tunnels) + (cavities)

An algorithm for evaluating the Euler number in a binary 3D image when 6-connectivity is assumed for the foreground is presented in [1],[2]. The algorithm traverses all object voxels and calculates their contribution b to the Euler number. The evaluation of this contribution is based on the values of voxels forming 2×2×2 cube around the voxel under the consideration. The values of this voxels are used to construct an index n to the lookup table given in the file table.csv in the Help folder. This lookup table stores the contributions of each voxel according to its neighborhood configuration. The Euler number of the foreground is evaluated by adding the contributions of all the object voxels.

[1] Pitas I, Nikolaidis N, “3-D image processing algorithms”, Wiley (2000).

[2] Chung-Nim L., Timothy P., Azriel R., “Winding and Euler numbers for 2D and 3D digital images”, CVGIP: Graphical Models and Image Processing (1991)
