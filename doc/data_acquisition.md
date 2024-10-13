# Data Acquisition

To download the dataset, run the following command:

```bash
python src/download_dataset.py
```

This will download the dataset from Google Drive. After downloading, the script will automatically unzip the dataset and remove any unnecessary metadata files.

## Manual Download

If the automatic download does not work, you can manually download the dataset from the following link:

[Download BrainTumourRaw.tar](https://drive.google.com/file/d/12XoMqhANCWrnFFrl-3cDmd9Xx_hVkJrk/view?usp=drive_link)

Once downloaded, rename the file to `BrainTumourRaw.tar` and place it in the `medical-image-segmentation` directory, and then run the script the following way:

```bash
python src/download_dataset.py --manual
```

## Preprocessing steps

In order to prepare medical imaging data and its corresponding segmentation for analysis, the following preprocessing steps are implemented. These steps ensure that the data is in a suitable format for subsequent processing and modeling.

1. **Load the original data and segmentation** from the specified file paths.
2. **Resize the image slices and the segmentation mask** to a specified dimension.
3. **Normalize the image data** to standardize the pixel values.
4. **Convert the segmentation mask** to one-hot encoding for use in classification tasks.
