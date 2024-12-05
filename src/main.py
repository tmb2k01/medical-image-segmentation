import os

import torch
from monai.losses import DiceLoss
from monai.networks.nets import UNETR, SegResNet
from pytorch_lightning import LightningModule, Trainer
from pytorch_lightning.callbacks import ModelCheckpoint

from src.dataloader import BrainTumourDataModule
from src.model.common import CommonPLModuleWrapper

IMAGE_PATH = "./data/BrainTumourData/imagesTr/"
LABEL_PATH = "./data/BrainTumourData/labelsTr/"
IMG_SIZE = 128
BATCH_SIZE = 1
IN_CHANNELS = 4
OUT_CHANNELS = 4


def _get_data_module() -> BrainTumourDataModule:
    data_module = BrainTumourDataModule(
        data_path=IMAGE_PATH,
        seg_path=LABEL_PATH,
        img_dim=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
    )
    data_module.prepare_data()
    data_module.setup()
    return data_module


def _train_model(
    model: LightningModule, data_module: BrainTumourDataModule, max_epochs: int = 1
) -> None:
    checkpoint_callback = ModelCheckpoint(
        monitor="val_loss",
        mode="min",
        save_top_k=1,
        dirpath="model/",
        filename=f"{model.__class__.__name__}",
    )
    trainer = Trainer(
        max_epochs=max_epochs,
        callbacks=[checkpoint_callback],
    )
    trainer.fit(model, data_module)


def _train() -> None:
    data_module = _get_data_module()

    # Train SegResNet
    segresnet_wrapper = CommonPLModuleWrapper(
        model=SegResNet(in_channels=IN_CHANNELS, out_channels=OUT_CHANNELS),
        loss_fn=DiceLoss(softmax=True),
    )
    _train_model(segresnet_wrapper, data_module)

    # Train UNETR
    unetr_wrapper = CommonPLModuleWrapper(
        model=UNETR(
            in_channels=IN_CHANNELS,
            out_channels=OUT_CHANNELS,
            img_size=(IMG_SIZE, IMG_SIZE, IMG_SIZE),
        ),
        loss_fn=DiceLoss(softmax=True),
    )
    _train_model(unetr_wrapper, data_module)


def _serve() -> None:
    pass


def _main() -> None:
    print(f"Is CUDA available: {torch.cuda.is_available()}")

    # Set the behavior based on the TRAIN_MODE environment variable.
    # If TRAIN_MODE is set to 1, the program runs in training mode.
    # Otherwise, it starts the application in serving mode.
    train_mode = int(os.environ["TRAIN_MODE"])
    print(f"TRAIN_MODE={train_mode}")
    if train_mode == 1:
        print("Starting up training...")
        _train()
    else:
        print("Loading model and serving requests...")
        _serve()


if __name__ == "__main__":
    _main()
