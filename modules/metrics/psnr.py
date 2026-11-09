import numpy as np

def calculate_mse(original, result):
    return float(np.mean((original.astype(np.float32) - result.astype(np.float32)) ** 2))

def calculate_psnr(original, result):
    mse = calculate_mse(original, result)
    return float("inf") if mse == 0 else float(10 * np.log10((255.0 ** 2) / mse))
