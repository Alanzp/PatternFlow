import cv2
import numpy as np
from processer.common.base import Base
from processer.common.parameter import Parameter


class OTSU_split(Base):
    def __init__(self):
        super().__init__()
        self.params["blurCoreSize"] = Parameter(current=5, min=3, max=100)
        self.params["erodeCoreSize"] = Parameter(current=7, min=3, max=100)

    def process(self, inputImage_BGR):
        ycrcb = cv2.cvtColor(inputImage_BGR,
                             cv2.COLOR_BGR2YCrCb)  # 把图像转换到YUV色域
        (_, cr, _) = cv2.split(ycrcb)  # 图像分割, 分别获取y, cr, br通道图像
        blurCoreSize = self.params["blurCoreSize"].getCurrent() // 2 * 2 + 1
        erodeCoreSize = self.params["erodeCoreSize"].getCurrent() // 2 * 2 + 1
        cr1 = cv2.GaussianBlur(cr, (blurCoreSize, blurCoreSize), 0)
        _, skin1 = cv2.threshold(cr1, 0, 255,
                                 cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        size = erodeCoreSize
        kernel = np.ones((size, size), dtype=np.uint8)
        erode_img = cv2.erode(skin1, kernel)
        skin2 = cv2.dilate(erode_img, kernel)
        skin3 = cv2.bitwise_and(inputImage_BGR, inputImage_BGR, mask=skin2)
        return skin3
