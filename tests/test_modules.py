import numpy as np
import pytest
from modules.filtering.service import parse_kernel, apply_custom_kernel
from modules.metrics.service import calculate_mse, calculate_psnr
from modules.color_analysis.service import convert_channels, calculate_histograms

def test_kernel_validation():
    assert parse_kernel("1,0,1
0,1,0
1,0,1").shape == (3, 3)
    with pytest.raises(ValueError): parse_kernel("1,0
0,1")
    with pytest.raises(ValueError, match="非數字"):
        parse_kernel("1,adf,1
0,1,0
1,0,1")

def test_filter_and_psnr_identity():
    image = np.full((8, 8, 3), 100, dtype=np.uint8)
    result = apply_custom_kernel(image, parse_kernel("0,0,0
0,1,0
0,0,0"))
    assert calculate_mse(image, result) == 0
    assert np.isinf(calculate_psnr(image, result))

def test_histogram_channels():
    image = np.zeros((4, 4, 3), dtype=np.uint8); image[:, :, 0] = 255
    _, channels = convert_channels(image, "RGB channels")
    hist = calculate_histograms(channels)
    assert hist["R"][255] == 16 and hist["G"][0] == 16
