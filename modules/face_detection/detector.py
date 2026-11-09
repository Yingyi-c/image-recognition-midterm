from pathlib import Path
import cv2

def load_detector():
    if not hasattr(cv2, "CascadeClassifier"):
        raise RuntimeError(
            "目前的 OpenCV 不包含 CascadeClassifier；請安裝 4.x 版本，"
            "不要使用目前的 OpenCV 5.0.0。"
        )
    detector = cv2.CascadeClassifier(str(Path(cv2.data.haarcascades) / "haarcascade_frontalface_default.xml"))
    if detector.empty():
        raise RuntimeError("無法載入 Haar Cascade 人臉分類器")
    return detector
