import gradio as gr
import nibabel as nib
import numpy as np
from PIL import Image

IMG_SIZE: int = 512
image_data: np.ndarray = None


def _slice_as_image(idx: int) -> Image:
    slice_data = image_data[:, :, idx - 1]
    slice_data = slice_data.astype(np.uint8)
    pil_image = Image.fromarray(slice_data)
    pil_image = pil_image.resize((IMG_SIZE, IMG_SIZE))
    return pil_image


def _empty_image() -> Image:
    return Image.fromarray(np.zeros((IMG_SIZE, IMG_SIZE), dtype=np.uint8))


def _make_segmentation(filepath: str, idx: int) -> Image:
    # TODO: @tmb2k01 This is where you should make the prediction
    # TODO: Make sure to preload the model somehow, don't load it each time
    global image_data

    if filepath is None:
        return _empty_image()

    mri_image = nib.load(filepath)
    image_data = mri_image.get_fdata()
    return _slice_as_image(idx)


def _change_slice(idx: int) -> Image:
    if image_data is None:
        return _empty_image()

    return _slice_as_image(idx)


def launch() -> None:
    with gr.Blocks() as ui:
        gr.Markdown("# Brain Tumor Segmentation 🧠")
        mri_file = gr.File(label="Upload MRI File", type="filepath")
        segmentation_button = gr.Button("Make Segmentation")
        slice_image = gr.Image(height=IMG_SIZE, label="MRI Slice")
        slice_slider = gr.Slider(label="Select MRI Slice", minimum=1, maximum=128)

        segmentation_button.click(
            fn=_make_segmentation,
            inputs=[mri_file, slice_slider],
            outputs=slice_image,
        )

        slice_slider.change(
            fn=_change_slice,
            inputs=[slice_slider],
            outputs=slice_image,
        )

    print("Launching gradio interface...")
    ui.launch(server_name="0.0.0.0", server_port=7860)


if __name__ == "__main__":
    launch()
