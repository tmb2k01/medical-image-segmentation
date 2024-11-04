import os
from pathlib import Path

import cv2
import nibabel as nib
import numpy as np
import pytorch_lightning as pl
import torch
import torch.nn.functional as F
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from util import is_power_of_two

root_dir = Path(__file__).parent.parent
TRAINING_DATA_PATH = f"{root_dir}/data/BrainTumourData/imagesTr/"
TRAINING_SEGMENTATION_PATH = f"{root_dir}/data/BrainTumourData/labelsTr/"

IMG_SIZE = 240


class BrainTumourDataset(Dataset):
    def __init__(
        self,
        data_path,
        seg_path,
        file_ids,
        img_dim=(IMG_SIZE, IMG_SIZE),
        transform=None,
    ):
        self.data_path = data_path
        self.seg_path = seg_path
        self.file_ids = file_ids
        self.dim = img_dim
        self.transform = transform
        self.n_channels = 2

    def __len__(self):
        return len(self.file_ids)

    def __getitem__(self, idx):
        file_id = self.file_ids[idx]
        X, y = self.__data_generation(file_id)

        X_shape = X.shape
        height = X_shape[1]
        width = X_shape[2]
        depth = X_shape[3]

        assert is_power_of_two(height), "MRI image height must be a power of two"
        assert is_power_of_two(width), "MRI image widht must be a power of two"
        assert is_power_of_two(depth), "MRI image depth must be a power of two"

        return X, y

    def __data_generation(self, file_id) -> torch.Tensor:
        data_path = os.path.join(self.data_path, file_id)
        seg_path = os.path.join(self.seg_path, file_id)

        data: np.ndarray = nib.load(data_path).get_fdata()
        seg: np.ndarray = nib.load(seg_path).get_fdata()

        # Assuming the shape of data is (H, W, D, C) where C = number of channels
        depth_orig = data.shape[2]
        depth_new = 128
        depth_diff = depth_orig - depth_new
        depth_start = depth_diff // 2
        depth_end = depth_orig - (depth_diff - depth_start)

        flair = data[:, :, depth_start:depth_end, 0]
        t1w = data[:, :, depth_start:depth_end, 1]
        t1gd = data[:, :, depth_start:depth_end, 2]
        t2w = data[:, :, depth_start:depth_end, 3]

        # Resize each slice properly to maintain the dimensions
        flair_resized = cv2.resize(flair, self.dim)
        t1w_resized = cv2.resize(t1w, self.dim)
        t1gd_resized = cv2.resize(t1gd, self.dim)
        t2w_resized = cv2.resize(t2w, self.dim)

        seg_resized = cv2.resize(seg, self.dim, interpolation=cv2.INTER_NEAREST)

        X = np.stack((flair_resized, t1w_resized, t1gd_resized, t2w_resized), axis=-1)

        # Standard normalization (mean and std)
        X_mean = np.mean(X, axis=(0, 1, 2))
        X_std = np.std(X, axis=(0, 1, 2))
        X_normalized = (X - X_mean) / (X_std + 1e-8)

        y = seg_resized[:, :, depth_start:depth_end]

        # Normalize and convert to tensors
        X_tensor = torch.from_numpy(X_normalized).permute(3, 0, 1, 2).float()
        y_tensor = torch.from_numpy(y).long()
        Y = F.one_hot(y_tensor, num_classes=4).permute(3, 0, 1, 2).float()

        return X_tensor, Y


class BrainTumourDataModule(pl.LightningDataModule):
    def __init__(
        self,
        data_path=TRAINING_DATA_PATH,
        seg_path=TRAINING_SEGMENTATION_PATH,
        batch_size=1,
        num_workers=4,
        img_dim=(IMG_SIZE, IMG_SIZE),
    ):
        super().__init__()
        self.data_path = data_path
        self.seg_path = seg_path
        self.batch_size = batch_size
        self.num_workers = num_workers
        self.img_dim = img_dim
        self.train_transform = transforms.Compose(
            [
                transforms.RandomHorizontalFlip(),
                transforms.RandomVerticalFlip(),
                transforms.ToTensor(),
            ]
        )
        self.train_ids = self.val_ids = self.test_ids = None

    def prepare_data(self):
        self.training_datas = [
            f.name for f in os.scandir(self.data_path) if f.is_file()
        ]

    def setup(self, stage=None):
        train_test_ids, val_ids = train_test_split(self.training_datas, test_size=0.2)
        train_ids, test_ids = train_test_split(train_test_ids, test_size=0.15)

        self.train_ids = train_ids
        self.val_ids = val_ids
        self.test_ids = test_ids

        # Create datasets for each split
        self.train_dataset = BrainTumourDataset(
            self.data_path,
            self.seg_path,
            self.train_ids,
            img_dim=self.img_dim,
            transform=self.train_transform,
        )
        self.val_dataset = BrainTumourDataset(
            self.data_path,
            self.seg_path,
            self.val_ids,
            img_dim=self.img_dim,
        )
        self.test_dataset = BrainTumourDataset(
            self.data_path,
            self.seg_path,
            self.test_ids,
            img_dim=self.img_dim,
        )

    def train_dataloader(self):
        return DataLoader(
            self.train_dataset,
            batch_size=self.batch_size,
            shuffle=True,
            num_workers=self.num_workers,
        )

    def val_dataloader(self):
        return DataLoader(
            self.val_dataset, batch_size=self.batch_size, num_workers=self.num_workers
        )

    def test_dataloader(self):
        return DataLoader(
            self.test_dataset, batch_size=self.batch_size, num_workers=self.num_workers
        )
