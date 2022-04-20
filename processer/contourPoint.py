import cv2
import numpy as np
from processer.common.base import Base
from processer.common.parameter import Parameter


class contourPoint(Base):
    def __init__(self):
        super().__init__()
        self.params["pointSize"] = Parameter(current=5, min=3, max=100)
        self.params["pointCount"] = Parameter(current=7, min=3, max=100)
        self.params["blurCoreSize"] = Parameter(current=5, min=3, max=100)
        self.params["erodeCoreSize"] = Parameter(current=7, min=3, max=100)

    def process(self, inputImage_BGR):
        ycrcb = cv2.cvtColor(inputImage_BGR,
                             cv2.COLOR_BGR2YCrCb)  # 把图像转换到YUV色域
        (_, cr, _) = cv2.split(ycrcb)  # 图像分割, 分别获取y, cr, br通道图像
        blurCoreSize = self.params["blurCoreSize"].getCurrent() // 2 * 2 + 1
        erodeCoreSize = self.params["erodeCoreSize"].getCurrent() // 2 * 2 + 1
        pointCount = self.params["pointCount"].getCurrent()
        pointSize = self.params["pointSize"].getCurrent()
        cr1 = cv2.GaussianBlur(cr, (blurCoreSize, blurCoreSize), 0)
        _, skin1 = cv2.threshold(cr1, 0, 255,
                                 cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        size = erodeCoreSize
        kernel = np.ones((size, size), dtype=np.uint8)
        erode_img = cv2.erode(skin1, kernel)
        skin2 = cv2.dilate(erode_img, kernel)
        contours, _ = cv2.findContours(skin2, cv2.RETR_TREE,
                                       cv2.CHAIN_APPROX_NONE)
        maxcont = contours[0]
        for cont in contours:
            if cont.shape[0] > maxcont.shape[0]:
                maxcont = cont
        step = int(maxcont.shape[0] / pointCount)
        contour = maxcont[::step]
        outImage = inputImage_BGR.copy()
        for point in contour:
            cv2.circle(outImage, (point[0][0], point[0][1]), pointSize,
                       (0, 0, 255), pointSize)
        M = cv2.moments(maxcont)
        cv2.circle(outImage,
                   (int(M['m10'] / M['m00']), int(M['m01'] / M['m00'])),
                   pointSize, (255, 0, 0), pointSize)
        return outImage
