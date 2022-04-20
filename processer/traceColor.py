import cv2
import numpy as np
from processer.common.base import Base
from processer.common.parameter import Parameter


class TraceColor(Base):
    def __init__(self):
        super().__init__()
        self.params["L_R"] = Parameter(current=150, min=0, max=255)
        self.params["L_G"] = Parameter(current=0, min=0, max=255)
        self.params["L_B"] = Parameter(current=0, min=0, max=255)
        self.params["U_R"] = Parameter(current=254, min=0, max=255)
        self.params["U_G"] = Parameter(current=0, min=0, max=255)
        self.params["U_B"] = Parameter(current=0, min=0, max=255)

    def process(self, inputImage_BGR):
        hsv_img = cv2.cvtColor(inputImage_BGR, cv2.COLOR_BGR2HSV)
        lowColor = np.uint8([[[
            self.params["L_B"].getCurrent(), self.params["L_G"].getCurrent(),
            self.params["L_R"].getCurrent()
        ]]])
        upperColor = np.uint8([[[
            self.params["U_R"].getCurrent(), self.params["U_G"].getCurrent(),
            self.params["U_B"].getCurrent()
        ]]])
        lowColor = cv2.cvtColor(lowColor, cv2.COLOR_BGR2HSV)
        upperColor = cv2.cvtColor(upperColor, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_img, lowColor, upperColor)
        output = cv2.bitwise_and(hsv_img, hsv_img, mask=mask)
        return output
