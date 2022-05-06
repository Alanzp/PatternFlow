import cv2
import numpy as np
from processer.common.base import Base
from processer.common.parameter import Parameter

INIT_ANGEL = 180


class Rotate(Base):
    def __init__(self):
        super().__init__()
        self.params["angle"] = Parameter(current=180, min=0, max=360)
        self.params["horizontalFlip"] = Parameter(current=0, min=0, max=1)
        self.params["verticalFlip"] = Parameter(current=0, min=0, max=1)

    def process(self, inputImage_BGR):
        angle = self.params["angle"].getCurrent() - INIT_ANGEL
        horizontalFlip = self.params["horizontalFlip"].getCurrent()
        verticalFlip = self.params["verticalFlip"].getCurrent()
        height, width, _ = inputImage_BGR.shape
        (cx, cy) = (width // 2, height // 2)
        rotationMatrix = cv2.getRotationMatrix2D((cx, cy), -angle, 1.0)
        cos = np.abs(rotationMatrix[0, 0])
        sin = np.abs(rotationMatrix[0, 1])
        newWidth = int((height * sin) + (width * cos))
        newHeight = int((height * cos) + (width * sin))
        rotationMatrix[0, 2] += (newWidth / 2) - cx
        rotationMatrix[1, 2] += (newHeight / 2) - cy
        image = cv2.warpAffine(inputImage_BGR, rotationMatrix,
                               (newWidth, newHeight))
        if horizontalFlip == 1:
            image = cv2.flip(image, 1)
        if verticalFlip == 1:
            image = cv2.flip(image, 0)
        return image
