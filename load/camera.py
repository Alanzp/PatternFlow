import cv2


class Camera:
    def __init__(self):
        self.capture = cv2.VideoCapture(0)

    def getCurrentFrame(self):
        if self.capture.isOpened():
            # Get one frame
            _, img = self.capture.read()
            # # Mirror flip
            img = cv2.flip(img, 1)
            return img
        return None

    def closeCamera(self):
        if hasattr(self, "capture"):
            self.capture.release()
