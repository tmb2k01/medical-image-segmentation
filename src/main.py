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
    checkpoint_callback = ModelCheckpoint(monitor="val_loss", mode="min")
    trainer = Trainer(
        max_epochs=max_epochs,
        callbacks=[checkpoint_callback],
    )
    trainer.fit(model, data_module)


def _main() -> None:
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


if __name__ == "__main__":
    _main()
