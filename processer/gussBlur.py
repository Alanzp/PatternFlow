import cv2
from processer.common.base import Base
from processer.common.parameter import Parameter


class GussBlur(Base):
    def __init__(self):
        super().__init__()
        self.params["sigma"] = Parameter(current=5, min=0, max=100)
        self.params["CoreSize"] = Parameter(current=9, min=3, max=100)

    def process(self, inputImage_BGR):
        size = self.params["CoreSize"].getCurrent() // 2 * 2 + 1
        kernel_size = (size, size)
        sigma = self.params["sigma"].getCurrent() / 10
        output = cv2.GaussianBlur(inputImage_BGR, kernel_size, sigma)
        return output
