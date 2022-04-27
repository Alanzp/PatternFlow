import cv2
import mediapipe as mp
import numpy as np
from processer.common.base import Base
from processer.common.parameter import Parameter

mp_drawing = mp.solutions.drawing_utils
mp_selfie_segmentation = mp.solutions.selfie_segmentation

BG_COLOR = (192, 192, 192)  # gray
MASK_COLOR = (255, 255, 255)  # white


class MediaPipeSelfieSegmentation(Base):
    def __init__(self):
        super().__init__()
        self.params["test"] = Parameter(current=5, min=0, max=100)
        # self.params["CoreSize"] = Parameter(current=9, min=3, max=100)

    def process(self, inputImage_BGR):
        with mp_selfie_segmentation.SelfieSegmentation(
                model_selection=0) as selfie_segmentation:
            results = selfie_segmentation.process(
                cv2.cvtColor(inputImage_BGR, cv2.COLOR_BGR2RGB))
            condition = np.stack(
                (results.segmentation_mask, ) * 3, axis=-1) > 0.1
            fg_image = np.zeros(inputImage_BGR.shape, dtype=np.uint8)
            fg_image[:] = MASK_COLOR
            bg_image = np.zeros(inputImage_BGR.shape, dtype=np.uint8)
            bg_image[:] = BG_COLOR
            output_image = np.where(condition, fg_image, bg_image)
            return output_image
