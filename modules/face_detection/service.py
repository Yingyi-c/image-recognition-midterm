import cv2
from common.types import FaceDetectionResult
from .detector import load_detector

def detect_faces(image, scale_factor=1.1, min_neighbors=5):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    faces = load_detector().detectMultiScale(gray, scaleFactor=scale_factor, minNeighbors=min_neighbors, minSize=(30, 30))
    output = image.copy(); boxes = []
    for index, (x, y, w, h) in enumerate(faces, 1):
        cv2.rectangle(output, (x, y), (x + w, y + h), (0, 220, 80), 3)
        cv2.putText(output, f"Face {index}", (x, max(20, y - 8)), cv2.FONT_HERSHEY_SIMPLEX, .7, (0, 180, 60), 2)
        boxes.append((int(x), int(y), int(w), int(h)))
    return FaceDetectionResult(len(boxes), boxes, None, output)
