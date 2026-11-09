from common.types import ImageMetadata

def get_metadata(filename, file_size, image):
    height, width = image.shape[:2]
    channels = image.shape[2] if image.ndim == 3 else 1
    return ImageMetadata(filename, width, height, channels, file_size)
