import cv2
import numpy as np


class ReconginizeFace():
    def __init__(self):
        # 参数0是初始值，参数1是参数范围
        self.casecade = cv2.CascadeClassifier(
            cv2.__path__[0] + r"\data\haarcascade_frontalface_default.xml")
        self.args = {
            "rec_width": [5, (0, 40)],
        }

    def outputStr(self):
        outputStr = ""
        for arg in self.args.keys():
            outputStr += arg + str(self.args[arg][0]) + ";"
        return outputStr

    def process(self, inputImage_BGR):
        gray_img = cv2.cvtColor(inputImage_BGR, cv2.COLOR_BGR2GRAY)
        haar_face = self.casecade.detectMultiScale(gray_img, 1.3, 5)
        rec_width = self.args["rec_width"][0]
        for (x, y, w, h) in haar_face:
            inputImage_BGR = cv2.rectangle(inputImage_BGR, (x, y),
                                           (x + w, y + h), (0, 0, 255),
                                           rec_width)
        return inputImage_BGR


class CannyLine():
    def __init__(self):
        # 参数0是初始值，参数1是参数范围
        self.args = {
            "threshold1": [100, (0, 255)],
            "threshold2": [200, (0, 255)]

            # "CoreSize":[5,()]
        }

    def outputStr(self):
        outputStr = ""
        for arg in self.args.keys():
            outputStr += arg + str(self.args[arg][0]) + ";"
        return outputStr

    def process(self, inputImage_BGR):
        th1 = self.args["threshold1"][0]
        th2 = self.args["threshold2"][0]
        print(th1, th2)
        grayImage = cv2.Canny(inputImage_BGR, th1, th2)
        output = cv2.cvtColor(grayImage, cv2.COLOR_GRAY2BGR)
        return output


class BGRCondition():
    def __init__(self):
        # 参数0是初始值，参数1是参数范围
        self.args = {
            "R": [0, (0, 254)],
            "G": [0, (0, 254)],
            "B": [0, (0, 254)]
        }

    def outputStr(self):
        outputStr = ""
        for arg in self.args.keys():
            outputStr += arg + str(self.args[arg][0]) + ";"
        return outputStr

    def process(self, inputImage_BGR):
        (B, G, R) = cv2.split(inputImage_BGR)
        B = B + self.args["B"][0]
        G = G + self.args["G"][0]
        R = R + self.args["R"][0]
        output = cv2.merge([B, G, R])
        return output


class GussBlur():
    def __init__(self):
        # 参数0是初始值，参数1是参数范围
        self.args = {"sigma": [5, (0, 100)], "CoreSize": [5, (3, 100)]}

    def outputStr(self):
        outputStr = ""
        for arg in self.args.keys():
            outputStr += arg + str(self.args[arg][0]) + ";"
        return outputStr

    def process(self, inputImage_BGR):
        size = self.args["CoreSize"][0] // 2 * 2 + 1
        kernel_size = (size, size)
        sigma = self.args["sigma"][0] / 10
        output = cv2.GaussianBlur(inputImage_BGR, kernel_size, sigma)
        return output


class OTSU_split():
    def __init__(self):
        # 参数0是初始值，参数1是参数范围
        self.args = {
            "blurCoreSize": [5, (3, 100)],
            "erodeCoreSize": [7, (3, 100)]
        }

    def outputStr(self):
        outputStr = ""
        for arg in self.args.keys():
            outputStr += arg + str(self.args[arg][0]) + ";"
        return outputStr

    def process(self, inputImage_BGR):
        ycrcb = cv2.cvtColor(inputImage_BGR,
                             cv2.COLOR_BGR2YCrCb)  # 把图像转换到YUV色域
        (y, cr, cb) = cv2.split(ycrcb)  # 图像分割, 分别获取y, cr, br通道图像
        blurCoreSize = self.args["blurCoreSize"][0] // 2 * 2 + 1
        erodeCoreSize = self.args["erodeCoreSize"][0] // 2 * 2 + 1
        cr1 = cv2.GaussianBlur(cr, (blurCoreSize, blurCoreSize), 0)
        _, skin1 = cv2.threshold(cr1, 0, 255,
                                 cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        size = erodeCoreSize
        kernel = np.ones((size, size), dtype=np.uint8)
        erode_img = cv2.erode(skin1, kernel)
        skin2 = cv2.dilate(erode_img, kernel)
        skin3 = cv2.bitwise_and(inputImage_BGR, inputImage_BGR, mask=skin2)
        return skin3


class TraceColor():
    def __init__(self):
        # 参数0是初始值，参数1是参数范围
        self.args = {
            "L_R": [150, (0, 255)],
            "L_G": [0, (0, 255)],
            "L_B": [0, (0, 255)],
            "U_R": [254, (0, 255)],
            "U_G": [0, (0, 255)],
            "U_B": [0, (0, 255)],
        }

    def outputStr(self):
        outputStr = ""
        for arg in self.args.keys():
            outputStr += arg + str(self.args[arg][0]) + ";"
        return outputStr

    def process(self, inputImage_BGR):
        hsv_img = cv2.cvtColor(inputImage_BGR, cv2.COLOR_BGR2HSV)

        lowColor = np.uint8(
            [[[self.args["L_B"][0], self.args["L_G"][0],
               self.args["L_R"][0]]]])
        upperColor = np.uint8(
            [[[self.args["U_B"][0], self.args["U_G"][0],
               self.args["U_R"][0]]]])
        lowColor = cv2.cvtColor(lowColor, cv2.COLOR_BGR2HSV)
        upperColor = cv2.cvtColor(upperColor, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_img, lowColor, upperColor)
        output = cv2.bitwise_and(hsv_img, hsv_img, mask=mask)
        return output


class BilateralFilter():
    def __init__(self):
        # 参数0是初始值，参数1是参数范围
        self.args = {
            "d": [1, (0, 10)],
            "sigmaColor": [5, (1, 100)],
            "sigmaSpace": [5, (1, 100)],
        }

    def outputStr(self):
        outputStr = ""
        for arg in self.args.keys():
            outputStr += arg + str(self.args[arg][0]) + ";"
        return outputStr

    def process(self, inputImage_BGR):
        output = cv2.bilateralFilter(inputImage_BGR, self.args["d"][0], self.args["sigmaColor"][0],
                                     self.args["sigmaSpace"][0])
        return output
