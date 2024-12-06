# User Guide

This document provides step-by-step instructions on how to build, start, and use the Gradio interface for performing brain tumor segmentation. The interface is backed by a pre-trained machine learning model. Below, you'll find information about running the Docker container, accessing the interface, and using its features.

## 1. Building and Running the Docker Container

### Quick Start

Run the following script to build and start the container:

```shell
./build_and_run.sh
```

This will build the Docker image and start the container. By default, this setup serves the Gradio interface for segmentation. **No training will occur in this step**.

### Using the Pre-Trained Model

The required model files have been uploaded to [this](https://drive.google.com/drive/folders/1UrRRhzHKyysyWa8uKfF43fvS9S7iuAHq?usp=sharing) Google Drive folder. If you prefer to skip the training process, simply download the two files and place them in the `model` folder. This will allow you to use the interface without the need for training. You can start making predictions immediately after launching the container.

### Training a Model (Optional)

If you want to train the model before serving the Gradio interface:

1. Run `build.sh` to build the Docker image.
2. Run the container with the --train flag to enable the training process:

    ```shell
    ./run.sh --train
    ```

## 2. Accessing the Gradio Interface

After the container is up and running, you will see the output logs in the terminal. Open a web browser and go to:

[http://localhost:7860](http://localhost:7860)

This will load the Gradio interface where you can interact with the model.

## 3. Using the Gradio Interface

### Upload the MRI File

On the interface, use the **Upload MRI File** section to upload an MRI scan. Three sample MRI files are provided in the `mri_image_examples` folder.

### Making a Segmentation

Once the file is uploaded, press the **Make Segmentation** button. This will run the model to generate a segmentation.

### View Different Slices

Use the slider labeled **Select MRI Slice** to navigate through the different slices of the segmented MRI. The segmentation results will update dynamically as you adjust the slider.

## 4. Additional Notes

* The segmentation results are displayed as images in the interface.
* The pre-trained model provided in the Google Drive folder ensures you can start using the system immediately without additional steps.
* Make sure the port `7860` is not blocked by a firewall to access the interface properly.
