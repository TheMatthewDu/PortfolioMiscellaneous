# Profile Picture Sketch Generator

This repository contains files that is used to convert a color image of an object to a rough sketch of the object.

Sample data can be found in [`data`](data)

## Notes
The current approach uses the `OpenCV` Python Library to perform image manipulations. It has the following pipeline:
* A Haar Cascade is used to identify features of concern
  * It uses a two Haar cascades in cases where features are less noticeable, such as in faces. In this case, the first cascade identifies the face and the second identifies the features
* Contours are identified in the object, which is drawn on a blank canvas (null matrix)
* This is repeated (except the last step with the null matrix, which is replaced as an accumulator) to get all facial features

The current approach has not yielded good results. Future attempts to better this design includes:
* Using Bézier curves to approximate the shapes of geometric shapes better
* Use of Canny (or another Edge Detector) to get better and cleaner edges for the sketch
* A color module, so colors can be extrapolated


