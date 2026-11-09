import numpy as np

def calculate_histograms(channels):
    return {name: np.bincount(np.clip(values.ravel(), 0, 255).astype(np.uint8), minlength=256) for name, values in channels.items()}
