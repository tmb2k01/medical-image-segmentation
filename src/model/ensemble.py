from typing import List

import torch
from pytorch_lightning import LightningModule
from torch import Tensor
from torch.nn.modules.loss import _Loss
from torch.optim import AdamW, Optimizer


class EnsembleModel(LightningModule):
    def __init__(self, model_list, num_classes):
        super(EnsembleModel, self).__init__()
        self.models: List[LightningModule] = model_list
        self.num_classes: int = num_classes

    def forward(self, x: Tensor) -> Tensor:
        for model in self.models:
            model.eval()

        predictions = [model(x) for model in self.models]
        return torch.mean(torch.stack(predictions), dim=0)
