Edge detection is the task of finding boundaries of objects in a digital image (2D or 3D) by detecting discontinuities in image intensity caused by the transition from one 3D region to another 3D region of different mean intensity. Note that although in 3D space the objects are bounded by surfaces, the terms edge and edge detection are still used in literature.

As a measure of edge activity we can use the gradient magnitude on a certain voxel:

![image](https://user-images.githubusercontent.com/15230238/142948554-190f3b1e-d383-4fbb-80cc-26b3f53060e3.png)

or equivalently we can use the L1 norm:

![image](https://user-images.githubusercontent.com/15230238/142948630-064cdab8-196f-4d33-ac48-f60b01e9785f.png)

where f(z,y,x) is voxel’s intensity.

Edge detection can be performed by convolving the 3D image with a set of three 3D Sobel masks. Each such mask acts as a discrete approximation of the partial derivative with respect to a specific direction. For example, such a 3×3×3 mask for the x-direction is the following:

![image](https://user-images.githubusercontent.com/15230238/142948672-0af5a8b2-7fba-4893-ae17-175a342dbe73.png)

[1] Pitas I, Nikolaidis N, “3-D image processing algorithms”, Wiley (2000).
