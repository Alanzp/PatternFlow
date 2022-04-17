import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

SAVE_IMAGE_SUFFIX = ".jpg"


def doSaveLocalFile(savePath: str, fileName: str, imageSave: np.ndarray):
    saveRoot = Path(savePath)
    plt.imsave(saveRoot.joinpath(fileName + SAVE_IMAGE_SUFFIX), imageSave)
