import cv2
from processer.common.base import Base
from processer.common.parameter import Parameter


class ReconginizeFace(Base):
    def __init__(self):
        super().__init__()
        self.casecade = cv2.CascadeClassifier(
            cv2.__path__[0] + r"\data\haarcascade_frontalface_default.xml")
        self.params["rec_width"] = Parameter(current=5, min=0, max=40)

    def process(self, inputImage_BGR):
        gray_img = cv2.cvtColor(inputImage_BGR, cv2.COLOR_BGR2GRAY)
        haar_face = self.casecade.detectMultiScale(gray_img, 1.3, 5)
        rec_width = self.params["rec_width"].getCurrent()
        for (x, y, w, h) in haar_face:
            inputImage_BGR = cv2.rectangle(inputImage_BGR, (x, y),
                                           (x + w, y + h), (0, 0, 255),
                                           rec_width)
        return inputImage_BGR
