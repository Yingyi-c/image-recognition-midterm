import numpy as np

def convert_channels(image: np.ndarray, mode: str):
    if mode == "Original":
        gray = np.clip(0.299 * image[:, :, 0] + 0.587 * image[:, :, 1] + 0.114 * image[:, :, 2], 0, 255).astype(np.uint8)
        return image, {"Gray": gray}
    if mode == "RGB channels":
        return image, dict(zip(("R", "G", "B"), (image[:, :, 0], image[:, :, 1], image[:, :, 2])))
    rgb = image.astype(np.float32)
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    y = 0.299 * r + 0.587 * g + 0.114 * b
    u = -0.169 * r - 0.331 * g + 0.500 * b + 128.0
    v = 0.500 * r - 0.419 * g - 0.081 * b + 128.0
    yuv = np.stack([y, u, v], axis=2)
    display = np.stack([
        y + 1.402 * (v - 128.0),
        y - 0.344 * (u - 128.0) - 0.714 * (v - 128.0),
        y + 1.772 * (u - 128.0),
    ], axis=2)
    display = np.clip(display, 0, 255).astype(np.uint8)
    channels = {name: np.clip(values, 0, 255).astype(np.uint8) for name, values in zip(("Y (亮度)", "U (色度)", "V (色度)"), (y, u, v))}
    return display, channels
