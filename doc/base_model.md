# Base Model

## Overview

In this project, we aim to establish a baseline model to compare the performance of more complex machine learning algorithms. The base model will be a simple intensity-based classifier that assigns pixels to different segments based on the mean intensity values associated with each type of brain segment. This approach does not involve any real machine learning; instead, it relies on a straightforward statistical analysis of pixel intensities.

## How the Model Works

The base model operates through a series of steps to classify MRI pixels based on their intensity values:

### 1. Calculating Mean Pixel Intensity

1. Extract Pixel Intensities
    For each segment type, we will extract the pixel intensity values from the training set.
1. Calculate Mean Intensity
    For each class $C_i$, compute the mean intesity as follows:

    ```math
    Mean Intensity_i=\frac 1{N_i}\sum_{j=1}^{N_i}I_j
    ```

    Where:
    * $N_i$ is the total number of pixels in class $C_i$
    * $I_j$ is the intensity value of pixel $j$

### 2. Classification

1. Assigning Pixels to Classes
    For each pixel *I* in an MRI image, classify it based on the closest mean intensity. Assign $I$ to class $C_k$ where $k$ by the following rule:

    ```math
    k=\argmin_i|I-MeanIntensity_i|
    ```

2. Output
   The model produces a segmented image where each pixel is labeled according to the class it belongs to, based on the nearest mean intensity comparison.
