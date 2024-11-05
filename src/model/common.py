from typing import Tuple

from pytorch_lightning import LightningModule
from torch import Tensor
from torch.nn import Module
from torch.nn.modules.loss import _Loss
from torch.optim import AdamW, Optimizer


class CommonPLModuleWrapper(LightningModule):
    def __init__(
        self,
        model: Module,
        loss_fn: _Loss,
        learning_rate: float = 1e-3,
    ) -> None:
        super(CommonPLModuleWrapper, self).__init__()
        self.model = model
        self.loss_fn = loss_fn
        self.learning_rate = learning_rate

    def forward(self, x: Tensor) -> Tensor:
        return self.model(x)

    def training_step(self, batch: Tuple[Tensor, Tensor], batch_idx: int) -> Tensor:
        loss, _ = self._common_step(batch, batch_idx)
        self.log("train_loss", loss, on_epoch=True)
        return loss

    def validation_step(self, batch, batch_idx):
        loss, _ = self._common_step(batch, batch_idx)
        self.log("val_loss", loss, prog_bar=True)
        return loss

    def _common_step(
        self, batch: Tuple[Tensor, Tensor], batch_idx: int
    ) -> Tuple[Tensor, Tensor]:
        images, labels = batch
        preds = self.forward(images)
        loss = self.loss_fn(preds, labels)
        return loss, preds

    def configure_optimizers(self) -> Optimizer:
        return AdamW(self.parameters(), lr=self.learning_rate)
