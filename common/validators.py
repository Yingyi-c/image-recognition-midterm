import numpy as np

def validate_kernel(kernel: np.ndarray) -> np.ndarray:
    kernel = np.asarray(kernel, dtype=np.float32)
    if kernel.ndim != 2 or kernel.shape[0] != kernel.shape[1]:
        raise ValueError("卷積核必須是二維方陣")
    if kernel.shape[0] < 1 or kernel.shape[0] % 2 == 0:
        raise ValueError("卷積核邊長必須是正奇數")
    if not np.isfinite(kernel).all():
        raise ValueError("卷積核不可包含無限大或非數值")
    return kernel
