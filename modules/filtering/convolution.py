import cv2
import numpy as np
from common.image_utils import bgr_to_rgb, ensure_uint8, rgb_to_bgr

def normalize_kernel(kernel):
    total = float(kernel.sum())
    return kernel / total if abs(total) > 1e-12 else kernel

def apply_kernel(image: np.ndarray, kernel: np.ndarray, normalize: bool = False) -> np.ndarray:
    used = normalize_kernel(kernel) if normalize else kernel
    result = cv2.filter2D(rgb_to_bgr(image), -1, used, borderType=cv2.BORDER_REFLECT)
    return ensure_uint8(bgr_to_rgb(result))
