from dataclasses import dataclass
from typing import Optional
import numpy as np

@dataclass
class ImageMetadata:
    filename: str
    width: int
    height: int
    channels: int
    file_size: int

@dataclass
class FaceDetectionResult:
    count: int
    boxes: list
    confidence: Optional[list]
    image: np.ndarray

@dataclass
class FilterResult:
    original: np.ndarray
    filtered: np.ndarray
    kernel: np.ndarray
    psnr: float
