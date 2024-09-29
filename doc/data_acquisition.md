# Data Acquisition

To download the dataset, run the following command:

```bash
python download_dataset.py
```

This will download the dataset from Google Drive. After downloading, the script will automatically unzip the dataset and remove any unnecessary metadata files.

## Manual Download

If the automatic download does not work, you can manually download the dataset from the following link:

[Download BrainTumourRaw.tar](https://drive.google.com/file/d/12XoMqhANCWrnFFrl-3cDmd9Xx_hVkJrk/view?usp=drive_link)

Once downloaded, rename the file to `BrainTumourRaw.tar` and place it in the `medical-image-segmentation` directory, and then run the script with the following command:

```bash
python download_dataset.py --manual
```
