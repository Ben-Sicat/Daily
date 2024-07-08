# Mask R-CNN for Object Detection and Segmentation using TensorFlow 2 (2.7.0)

## Introduction
The [mask-rcnn-tf2-us](https://github.com/mrk1992/mask-rcnn-tf2-us) project edits the original [Mask_RCNN](https://github.com/matterport/Mask_RCNN) project, which only supports TensorFlow 1.0, so that it works on TensorFlow 2 (Especially 2.7.0). Based on this new project, the [Mask R-CNN](https://arxiv.org/abs/1703.06870) can be trained and tested (i.e make predictions) in TensorFlow 2. The Mask R-CNN model generates bounding boxes and segmentation masks for each instance of an object in the image. It's based on Feature Pyramid Network (FPN) and a ResNet101 backbone.

### Heres how we'll approach the Segmentation part

**1. Simplify the Scope:**

* **Start with Single Food Items:** Focus on estimating the volume of one food item per image. This simplifies segmentation and volume calculations.
* **Limit Food Variety Initially:** Choose a few food types with distinct and relatively consistent shapes (e.g., sliced bread, bananas, apples). This helps in validating your model's accuracy.
* **Controlled Environment:** Capture your initial images in a controlled environment (good lighting, consistent background) to reduce noise and variation.

**2. Pinhole Camera Model Development:**

You don't necessarily need machine learning (like SVM) for the pinhole camera model itself. This part is primarily geometric. Here's how to approach it:

* **Camera Calibration (Optional, but Recommended):**
* While you can use the plate as a reference, calibrating your camera intrinsics (focal length, principal point, distortion coefficients) will improve accuracy.
* You can use a calibration target (like a checkerboard) or even your plate with known dimensions. Libraries like OpenCV make this process straightforward.
* **Establish Reference Points:**
* **Plate:** Detect the plate's edges in the image (using edge detection or your Mask R-CNN). Calculate its real-world dimensions (length and width) and its position relative to the camera.
* **Food:** After segmentation with Mask R-CNN, identify key points on the food item (topmost, bottommost, leftmost, rightmost points) in the image.

* **Depth Information:**
* Use your depth image to get the distance (z-coordinate) of the reference points (on the food and plate) from the camera.

* **3D Point Calculation (Pinhole Camera Model):**
* With the camera intrinsics (if calibrated), depth information, and image coordinates, you can use the pinhole camera equations to calculate the 3D coordinates (X, Y, Z) of the reference points in the real world.

**3. Volume Estimation:**

* **Geometric Approximation:**
* Once you have the 3D points, you can approximate the food shape using simple geometric primitives:
* **Ellipsoid:** A good approximation for many fruits.
* **Cylinder:** Suitable for foods with a circular base (e.g., a glass of water).
* **Cone:** For conical shapes.
* **Combination:** For more complex shapes, you can divide the segmented food into smaller, simpler shapes.
* **Volume Calculation:** Use the standard volume formulas for the chosen geometric primitive(s).

**Example:** Let's say you have a banana.

1. **Segmentation:** Use Mask R-CNN to get a mask of the banana.
2. **Reference Points:** Find the top, bottom, leftmost, and rightmost points of the banana in the image.
3. **Depth:** Obtain the depth values at those points from the depth image.
4. **3D Points:** Use the pinhole camera model to calculate the 3D coordinates of the reference points.
5. **Approximation:** Approximate the banana shape as an ellipsoid using the 3D points.
6. **Volume:** Calculate the volume of the ellipsoid.

**Limited Depth Data:**

You mentioned limited depth data. Here are some strategies:

* **Depth Completion:** If your depth images have holes or are low resolution, you can use depth completion algorithms (many are deep learning-based) to fill in the missing information.
* **Shape from Shading/Structure from Motion:** Explore these techniques as alternatives or complements to depth information. They can infer 3D structure from 2D images.

**Code Structure:**

```python
import cv2 # For image processing
import numpy as np

# 1. Load and Preprocess Images:
rgb_image = cv2.imread("food_image.jpg")
depth_image = cv2.imread("depth_image.png", cv2.IMREAD_ANYDEPTH)

# 2. Food and Plate Detection & Segmentation (Mask R-CNN):
# ... (Your existing code for Mask R-CNN) ...

# 3. Camera Model and 3D Point Calculation:
# ... (Implement pinhole camera model equations - see OpenCV documentation) ...

# 4. Volume Estimation:
# ... (Calculate volume using geometric approximation) ...
```

**Additional Tips:**

* **Evaluation:** Use objects with known volumes to thoroughly evaluate your algorithm's accuracy.
* **Datasets:** Look for publicly available datasets that include food images with depth or 3D annotations. Even if they don't perfectly match your use case, they can be helpful for pre-training or fine-tuning models.
* **Synthetic Data:** Consider generating synthetic depth images or 3D models of food to supplement your limited data.


This project is tested against **tensorflow-gpu 2.7.0**, **keras 2.7.0-tf**, and **python 3.8.12**. Note that the project will not run in TensorFlow 1.0.


## Environment for Linux
~~~
cuda==11.2
cudnn==8.2.0
tensorflow-gpu==2.7.0  
conda==4.12.0
~~~

## Reference
https://github.com/matterport/Mask_RCNN  
https://github.com/ahmedfgad/Mask-RCNN-TF2
