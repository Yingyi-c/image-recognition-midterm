from PIL import Image
import numpy as np

SUPPORTED_FORMATS = {"png", "jpg", "jpeg", "bmp"}

def load_image(uploaded_file) -> np.ndarray:
    return np.array(Image.open(uploaded_file).convert("RGB"))
