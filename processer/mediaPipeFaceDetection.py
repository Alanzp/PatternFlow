import cv2
import mediapipe as mp
from processer.common.base import Base
from processer.common.parameter import Parameter

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils


class MediaPipeFaceDetection(Base):
    def __init__(self):
        super().__init__()
        self.params["test"] = Parameter(current=5, min=0, max=100)
        # self.params["CoreSize"] = Parameter(current=9, min=3, max=100)

    def process(self, inputImage_BGR):
        with mp_face_detection.FaceDetection(
                model_selection=1,
                min_detection_confidence=0.5) as face_detection:
            results = face_detection.process(
                cv2.cvtColor(inputImage_BGR, cv2.COLOR_BGR2RGB))
            # Draw face detections of each face.
            if not results.detections:
                return inputImage_BGR
            annotated_image = inputImage_BGR.copy()
            for detection in results.detections:
                mp_drawing.draw_detection(annotated_image, detection)
            return annotated_image
