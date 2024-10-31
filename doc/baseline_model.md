# Baseline Model

## Overview

In this project, we aim to establish a baseline model to compare the performance of more complex machine learning algorithms. The baseline model will be a simple intensity-based classifier that assigns pixels to different segments based on the mean intensity values associated with each type of brain segment. This approach does not involve any real machine learning; instead, it relies on a straightforward statistical analysis of pixel intensities.

## How the Model Works

The baseline model operates through a series of steps to classify MRI pixels based on their intensity values:

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
    For each pixel $I$ in an MRI image, we classify it based on a comparison with the computed mean intensities. Each pixel is assigned to a class $C_k$ where $k$ is determined by the following rule:

    ```math
    k=\argmin_i|I-MeanIntensity_i|
    ```

    This means that a pixel is classified into the class corresponding to the closest mean intensity.

2. Thresholding for Background Class
    In addition to the nearest mean intensity comparison, any pixel with an intensity less than the mean intensity of the first class will be assigned to the Background class by default. This ensures that non-tumorous tissues are identified somewhat well.

3. Output
    The model produces a segmented image where each pixel is labeled according to the class it belongs to, based on the nearest mean intensity comparison and thresholding for the Background class. The final output is a 4D tensor representing the one-hot encoded class labels for each pixel in the input images.

## Model Performance Evaluation

The baseline model's performance shows a substantial gap in its ability to detect and differentiate tumor classes, which is expected given the simplistic approach used. Analyzing the key metrics helps us understand the model's current limitations and where improvements should be made.

### Dice Score

The Dice Score, crucial in segmentation tasks, gauges how well the predicted masks align with the ground truth, with higher values indicating better overlap. In this evaluation, the model achieves a Dice Score of 0.988 for the Background class, showing it successfully segments background pixels with minimal error. However, for the three tumor-related classes the Dice Scores are close to zero, save for a marginal 0.1015 score for Enhancing Tumor. The mean Dice Score of 0.272 highlights that the model predominantly labels pixels as background, struggling to effectively segment tumor areas.

### Precision and Recall

Precision and Recall offer additional insight into the model's class discrimination. Precision reflects how accurately the model's predictions match the ground truth, while Recall indicates the model's success in capturing all relevant pixels for each class. The high Precision (0.9935) and Recall (0.9834) for the Background class confirm that the model correctly identifies nearly all background pixels, with low false positives. However, the remaining classes, particularly the tumor types, show near-zero Precision and Recall, except for a moderate Recall of 0.499 for Enhancing Tumor, meaning the model correctly captures approximately half of the enhancing tumor pixels. The low Precision for Enhancing Tumor (0.0565), however, suggests that many of these predictions are inaccurate, resulting in a high rate of false positives.

Interestingly, the recall for Enhancing Tumor provides a slight edge over random chance, which could imply the baseline model is not entirely arbitrary in recognizing this class. However, it's evident that the simplistic intensity-based approach lacks the complexity needed to distinguish the intricate features of tumor regions.

### Confusion Matrix

The confusion matrix further illustrates the baseline model's performance limitations. Most of the model's predictions fall into the Background class, with only a small proportion correctly attributed to tumor classes. Enhancing Tumor has a correct pixel count of 191,274, while misclassifications are prevalent, especially with tumor pixels classified incorrectly as background. This outcome highlights the baseline model's bias toward the dominant background class, likely due to the overwhelming presence of background pixels relative to tumor regions.

### Summary

In summary, the baseline model, as an intensity-based classifier, achieves high accuracy in detecting background pixels but lacks the complexity to reliably identify tumor regions. This foundational analysis underscores the need for more advanced segmentation models, such as deep learning architectures that can capture the nuanced features necessary for distinguishing between various brain tumor types.
