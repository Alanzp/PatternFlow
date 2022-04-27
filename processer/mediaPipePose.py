import cv2
import mediapipe as mp
import numpy as np
from processer.common.base import Base
from processer.common.parameter import Parameter

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

BG_COLOR = (192, 192, 192)  # gray


class MediaPipePose(Base):
    def __init__(self):
        super().__init__()
        self.params["test"] = Parameter(current=5, min=0, max=100)
        # self.params["CoreSize"] = Parameter(current=9, min=3, max=100)

    def process(self, inputImage_BGR):
        with mp_pose.Pose(static_image_mode=True,
                          model_complexity=2,
                          enable_segmentation=True,
                          min_detection_confidence=0.5) as pose:
            results = pose.process(
                cv2.cvtColor(inputImage_BGR, cv2.COLOR_BGR2RGB))
            annotated_image = inputImage_BGR.copy()
            if not results.pose_landmarks:
                return inputImage_BGR
            condition = np.stack(
                (results.segmentation_mask, ) * 3, axis=-1) > 0.1
            bg_image = np.zeros(inputImage_BGR.shape, dtype=np.uint8)
            bg_image[:] = BG_COLOR
            annotated_image = np.where(condition, annotated_image, bg_image)
            mp_drawing.draw_landmarks(annotated_image,
                                      results.pose_landmarks,
                                      mp_pose.POSE_CONNECTIONS,
                                      landmark_drawing_spec=mp_drawing_styles.
                                      get_default_pose_landmarks_style())
            return annotated_image
