import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import time

SAVE_IMAGE_SUFFIX = ".png"
SUFFIX_SYMBOL = "."


def doSaveLocalFile(savePath: str, fileName: str, imageSave: np.ndarray):
    saveRoot = Path(savePath)
    if fileName.find(SUFFIX_SYMBOL) != -1:
        fileName = "".join(fileName.split(SUFFIX_SYMBOL)[:-1])
    plt.imsave(saveRoot.joinpath(fileName + SAVE_IMAGE_SUFFIX), imageSave)


def genCaptureFileName():
    return "capture_{}".format(int(time.time()))
