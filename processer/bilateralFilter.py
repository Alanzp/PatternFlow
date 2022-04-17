import cv2
from processer.common.base import Base
from processer.common.parameter import Parameter


class BilateralFilter(Base):
    def __init__(self):
        super().__init__()
        self.params["d"] = Parameter(current=1, min=0, max=10)
        self.params["sigmaColor"] = Parameter(current=5, min=1, max=100)
        self.params["sigmaSpace"] = Parameter(current=5, min=1, max=100)

    def process(self, inputImage_BGR):
        output = cv2.bilateralFilter(inputImage_BGR,
                                     self.params["d"].getCurrent(),
                                     self.params["sigmaColor"].getCurrent(),
                                     self.params["sigmaSpace"].getCurrent())
        return output
