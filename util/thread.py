import time
from PyQt5.QtCore import pyqtSignal, QThread
import numpy as np


class MyThread(QThread):
    sinOut = pyqtSignal(np.ndarray)
    timeCost = 0

    def __init__(self, process_func, img):
        super().__init__()
        self.process_func = process_func
        self.img = img

    def run(self):
        startTime = time.time()
        self.outputImg = self.process_func(self.img)
        endTime = time.time()
        MyThread.timeCost = (endTime - startTime) * 10**3
        self.sinOut.emit(self.outputImg)
