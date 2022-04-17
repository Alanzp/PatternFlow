import cv2
from processer.common.base import Base
from processer.common.parameter import Parameter


class CannyLine(Base):
    def __init__(self):
        super().__init__()
        self.params["threshold1"] = Parameter(current=100, min=0, max=255)
        self.params["threshold2"] = Parameter(current=200, min=0, max=255)

    def process(self, inputImage_BGR):
        th1 = self.params["threshold1"].getCurrent()
        th2 = self.params["threshold2"].getCurrent()
        grayImage = cv2.Canny(inputImage_BGR, th1, th2)
        output = cv2.cvtColor(grayImage, cv2.COLOR_GRAY2BGR)
        return output
