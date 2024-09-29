# Evaluation Criteria

## Overview

In this project, we are dealing with four distinct types of brain segments:

1. Background (healthy tissue)
2. Edema (swelling around the tumor)
3. Non-Enhancing Tumor (tumor segments that don't actively absorb contrast agents)
4. Enhancing Tumor (actively growing and contrast-absorbing tumor regions)

Given this, our model's task is to segment these four classes as accurately as possible. Our evaluation criteria will account for the performance across each region individually, while still emphasizing recall to avoid missing any tumor regions (especially the more critical tumor classes).

## Evaluation Metrics

### 1. Dice Similarity Coefficient (DSC)

The *Dice Score* can be calculated separately for each type of brain segment. This allows us to measure how well the model recognizes each region individually.

For each class, we calculate the following:

```math
DSC_i=\frac{2\cdot|P_i\cap T_i|}{|P_i|+|T_i|}
```

Where:

* $P_i$ is the set of *predicted* pixels for each class
* $T_i$ is the set of *ground truth* pixels for each class

In this case a high *Dice Score* for each type indicates that the model has good overlap between the predicted and actual segmentations.

### 2. Mean Dice Score

To summarize performance across all four classes, we calculate the *Mean Dice Score*. This gives us an overall sense of how well our model is doing. This metric is calculated with the following formula:

```math
Mean DSC=\frac 14\sum_{i=1}^4DSC_i
```

### 3. Recall

Since we want to prioritize *Recall* for the tumor regions to ensure we don't miss any truly sick patients, we will compute recall separately for each tumor class.

We calculate the following for each type of tumor:

```math
Recall_i=\frac{TP_i}{TP_i+FN_i}
```

Where:

* $TP_i$ is the number of correctly classified pixels
* $FN_i$ is the number of pixels that belong to class $i$, but were missed by the model

We consider, that in this domain, the *Recall* value is of critical importance. Missing any of these regions could result in a serious error, espacially if we miss a region with enhancing tumor. Our goal is to maximize recall for these regions even if it leads to more false positive predictions.

### 4. Precision

Precision measures how many of the predicted pixels are correctly identified.

For each type of brain region, we calculate:

```math
Precision_i=\frac{TP_i}{TP_i+FP_i}
```

Where:

* $TP_i$ is the number of correctly classified pixels
* $FP_i$ is the number of incorrectly classified pixels

While *Precision* can be a rather important metric, we are willing to sacrifice it in favor of higher a *Recall* value.

### 5. Weighted Recall

Incorrectly classifying a healthy pixel is not as problematic as misclassifying an enhancing tumor pixel. To better understand how our model performs in this regard, we will calculate a *Weighted Recall*.

We will give more significance to tumor pixels than to healthy ones. To do so, we compute the following:

```math
WeightedRecall=\alpha_1\cdot Recall_{edema}+\alpha_2\cdot Recall_{non-enhancing}+\alpha_3\cdot Recall_{enhancing}
```

Where the $\alpha_i$ weights can be adjusted based on the importance assigned to each type of tumor tissue. Typically, we expect that $\alpha_1 \leq \alpha_2 \leq \alpha_3$ will hold true, giving the highest priority to enhancing tumor pixels.

### 6. Confusion Matrix

A multi-class confusion matrix provides a clear overview of how well the model distinguishes between the four types of tissues. It shows where the model tends to make mistakes &mdash; whether it's confusing one tumor class with another or missing tumor pixels altogether. This metric will be useful for understanding how the model operates behind the scenes and to help avoid critical errors, such as failing to detect tumor tissue.

## Prioritizing Critical Tissue Types

While we evaluate all tissue types using the metrics above, our primary focus is on identifying tumor classes:

* Non-Enhancing Tumor
* Enhancing Tumor (highest priority)

*Recall* for these classes will be the most important metric, especially for the enhancing tumor, which represents the most aggressive tumor type. Our goal is to fine-tune the model to maximize recall for these tumor types while also balancing its overall performance.
