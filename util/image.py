import cv2
from PyQt5.QtGui import QImage
from PyQt5.QtCore import Qt, QSize
import numpy as np
"""
  solved opencv image channel gap with QT frame
"""


def convertBGR2RGB(img: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


def convertRGB2BGR(img: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)


def convertCV2QImg(img: np.ndarray) -> QImage:
    rows, cols, channels = img.shape
    bytesPerLine = channels * cols
    QImg = QImage(img.data, cols, rows, bytesPerLine, QImage.Format_RGB888)
    return QImg


def imageFormatForShow(img: np.ndarray, size: QSize) -> QImage:
    QImg = convertCV2QImg(img)
    return QImg.scaled(size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
