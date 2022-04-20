import cv2
from processer.common.base import Base
from processer.common.parameter import Parameter


class ConditionBGR(Base):
    def __init__(self):
        super().__init__()
        self.params["R"] = Parameter(current=0, min=0, max=254)
        self.params["G"] = Parameter(current=0, min=0, max=254)
        self.params["B"] = Parameter(current=0, min=0, max=254)

    def process(self, inputImage_BGR):
        (B, G, R) = cv2.split(inputImage_BGR)
        B = B + self.params["B"].getCurrent()
        G = G + self.params["G"].getCurrent()
        R = R + self.params["R"].getCurrent()
        output = cv2.merge([B, G, R])
        return output
