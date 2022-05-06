from processer.common.base import Base
from processer.common.parameter import Parameter

MIN_CUT_SIZE = 5


class CutPicture(Base):
    def __init__(self):
        super().__init__()
        self.params["top"] = Parameter(current=0, min=0, max=10000)
        self.params["bottom"] = Parameter(current=0, min=0, max=10000)
        self.params["left"] = Parameter(current=0, min=0, max=10000)
        self.params["right"] = Parameter(current=0, min=0, max=10000)

    def process(self, inputImage_BGR):
        left = self.params["left"].getCurrent()
        right = self.params["right"].getCurrent()
        top = self.params["top"].getCurrent()
        bottom = self.params["bottom"].getCurrent()
        heigh, width, _ = inputImage_BGR.shape
        left = max(min(left, width - right - MIN_CUT_SIZE), 0)
        right = max(min(right, width - left - MIN_CUT_SIZE), 0)
        top = max(min(top, heigh - bottom - MIN_CUT_SIZE), 0)
        bottom = max(min(bottom, heigh - top - MIN_CUT_SIZE), 0)
        cutImage = inputImage_BGR[top:heigh - bottom, left:width - right]
        return cutImage
