import cv2
import gradio as gr
import nibabel as nib
import numpy as np
import torch
from monai.losses import DiceLoss
from monai.networks.nets import UNETR, SegResNet
from PIL import Image
from src.model.common import CommonPLModuleWrapper
from src.model.ensemble import EnsembleModel

IMG_SIZE: int = 512
INPUT_SIZE = 128
BATCH_SIZE = 1
IN_CHANNELS = 4
OUT_CHANNELS = 4
image_data: np.ndarray = None
segmentation_data: np.ndarray = None
model: EnsembleModel = None


def _slice_as_image(idx: int, image: np.ndarray) -> Image:
    slice_data = image[:, :, idx - 1]
    slice_data = slice_data.astype(np.uint8)
    pil_image = Image.fromarray(slice_data)
    pil_image = pil_image.resize((IMG_SIZE, IMG_SIZE))
    return pil_image.convert("L")


def _seg_as_image(idx: int, image: np.ndarray) -> Image:
    colors = {
        0: [68, 0, 84],  # Background - #440054
        1: [59, 82, 139],  # Edema - #3b528b
        2: [24, 184, 128],  # Non-enhancing Tumor - #18b880
        3: [230, 215, 79],  # Enhancing Tumor - #e6d74f
    }

    slice_data = image[:, :, idx - 1]
    color_image = np.zeros(
        (slice_data.shape[0], slice_data.shape[1], 3), dtype=np.uint8
    )

    # Define colors for each class

    for class_idx, color in colors.items():
        mask = slice_data == class_idx
        color_image[mask] = color

    pil_image = Image.fromarray(color_image)
    pil_image = pil_image.resize((IMG_SIZE, IMG_SIZE))
    return pil_image


def _empty_image() -> Image:
    return Image.fromarray(np.zeros((IMG_SIZE, IMG_SIZE), dtype=np.uint8))


def _make_segmentation(filepath: str, idx: int) -> Image:
    global image_data
    global segmentation_data

    if filepath is None:
        return _empty_image(), _empty_image()

    image_data = nib.load(filepath).get_fdata()
    X = _image_prepare(image_data)
    output = torch.argmax(model(X)[0], dim=0)
    segmentation_data = output.detach().cpu().numpy()
    unique_values = np.unique(segmentation_data)
    print(f"Unique values in segmentation data: {unique_values}")
    return _slice_as_image(idx, image_data[:, :, :, 0]), _seg_as_image(
        idx, segmentation_data
    )


def _change_slice(idx: int) -> Image:
    if image_data is None:
        return _empty_image(), _empty_image()

    return _slice_as_image(idx, image_data), _seg_as_image(idx, segmentation_data)


def _load_model() -> EnsembleModel:
    global model

    segresnet = CommonPLModuleWrapper(
        model=SegResNet(in_channels=IN_CHANNELS, out_channels=OUT_CHANNELS),
        loss_fn=DiceLoss(softmax=True),
    )
    segres_weights = torch.load(
        f"model/{segresnet.model.__class__.__name__}.ckpt", weights_only=True
    )
    segresnet.load_state_dict(segres_weights["state_dict"])

    unet = CommonPLModuleWrapper(
        model=UNETR(
            in_channels=IN_CHANNELS,
            out_channels=OUT_CHANNELS,
            img_size=(INPUT_SIZE, INPUT_SIZE, INPUT_SIZE),
        ),
        loss_fn=DiceLoss(softmax=True),
    )
    unet_weights = torch.load(
        f"model/{unet.model.__class__.__name__}.ckpt", weights_only=True
    )
    unet.load_state_dict(unet_weights["state_dict"])

    model = EnsembleModel([segresnet, unet], num_classes=4)


def _image_prepare(data: np.ndarray) -> torch.Tensor:
    depth_orig = data.shape[2]
    depth_new = 128
    depth_diff = depth_orig - depth_new
    depth_start = depth_diff // 2
    depth_end = depth_orig - (depth_diff - depth_start)

    flair = data[:, :, depth_start:depth_end, 0]
    t1w = data[:, :, depth_start:depth_end, 1]
    t1gd = data[:, :, depth_start:depth_end, 2]
    t2w = data[:, :, depth_start:depth_end, 3]

    flair_resized = cv2.resize(flair, (INPUT_SIZE, INPUT_SIZE))
    t1w_resized = cv2.resize(t1w, (INPUT_SIZE, INPUT_SIZE))
    t1gd_resized = cv2.resize(t1gd, (INPUT_SIZE, INPUT_SIZE))
    t2w_resized = cv2.resize(t2w, (INPUT_SIZE, INPUT_SIZE))

    X = np.stack((flair_resized, t1w_resized, t1gd_resized, t2w_resized), axis=-1)

    X_mean = np.mean(X, axis=(0, 1, 2))
    X_std = np.std(X, axis=(0, 1, 2))
    X_normalized = (X - X_mean) / (X_std + 1e-8)

    X_tensor = torch.from_numpy(X_normalized).permute(3, 0, 1, 2).float()
    X_tensor = X_tensor.unsqueeze(0)
    return X_tensor


def launch() -> None:
    _load_model()
    with gr.Blocks() as ui:
        gr.Markdown("# Brain Tumor Segmentation 🧠")
        mri_file = gr.File(label="Upload MRI File", type="filepath")
        segmentation_button = gr.Button("Make Segmentation")
        with gr.Row():
            slice_image = gr.Image(height=IMG_SIZE, label="MRI Slice")
            slice_segmentation = gr.Image(height=IMG_SIZE, label="Segmentation Slice")
        gr.Textbox(
            """
            🟣 Background
            🔵 Edema
            🟢 Non-enhancing Tumor
            🟡 Enhancing Tumor
            """,
            label="Legend",
        )
        slice_slider = gr.Slider(label="Select MRI Slice", minimum=1, maximum=128)

        segmentation_button.click(
            fn=_make_segmentation,
            inputs=[mri_file, slice_slider],
            outputs=[slice_image, slice_segmentation],
        )

        slice_slider.change(
            fn=_change_slice,
            inputs=[slice_slider],
            outputs=[slice_image, slice_segmentation],
        )

    print("Launching gradio interface...")
    ui.launch(server_name="0.0.0.0", server_port=7860)


if __name__ == "__main__":
    launch()
