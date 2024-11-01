import numpy as np
import torch
from sklearn.metrics import confusion_matrix
from typing import Tuple


def dice_score(preds: torch.Tensor, targets: torch.Tensor, eps: float = 1e-6) -> float:
    num_classes = preds.shape[2]
    dice_scores = []

    for i in range(num_classes):
        pred_flat = preds[:, :, i, :, :].contiguous().view(-1)
        target_flat = targets[:, :, i, :, :].contiguous().view(-1)

        intersection = (pred_flat * target_flat).sum().float()
        dice = (2.0 * intersection) / (pred_flat.sum() + target_flat.sum() + eps)
        dice_scores.append(dice.item())

    return dice_scores


def mean_dice_score(dice_scores: list) -> float:
    return sum(dice_scores) / len(dice_scores)


def recall_precision(preds: torch.Tensor, targets: torch.Tensor) -> Tuple[list, list]:
    num_classes = preds.shape[2]
    recall_scores = []
    precision_scores = []

    for i in range(num_classes):
        pred_flat = preds[:, :, i, :, :].contiguous().view(-1)
        target_flat = targets[:, :, i, :, :].contiguous().view(-1)

        tp = (pred_flat * target_flat).sum().float()
        fn = (target_flat * (1 - pred_flat)).sum().float()
        fp = (pred_flat * (1 - target_flat)).sum().float()

        recall = tp / (tp + fn + 1e-6)
        precision = tp / (tp + fp + 1e-6)

        recall_scores.append(recall.item())
        precision_scores.append(precision.item())

    return recall_scores, precision_scores


def weighted_recall(recall_scores: list, alpha: list) -> float:
    return sum([alpha[i] * recall_scores[i + 1] for i in range(len(alpha))])


def compute_confusion_matrix(preds: torch.Tensor, targets: torch.Tensor) -> np.ndarray:
    predicted_classes = torch.argmax(preds, dim=2).flatten().cpu().numpy()
    target_classes = torch.argmax(targets, dim=2).flatten().cpu().numpy()

    return confusion_matrix(target_classes, predicted_classes)
