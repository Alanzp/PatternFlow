"""
basic file process toolkit
"""

from export.localFile import SUFFIX_SYMBOL
import cv2
import numpy as np
from pathlib import Path

SUPPORT_IMAGR_SUFFIXES = ["*.jpg", "*.png", "*.jpeg", "*.bmp", "*.jpe"]


# solved opencv import image effected chinese path
def importImageFile(path: str):
    img = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
    if path.split(SUFFIX_SYMBOL)[-1] == "png":
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
    return img


def getImagePaths(dir: str):
    paths: list[str] = []
    for suffix in SUPPORT_IMAGR_SUFFIXES:
        paths.extend([path for path in Path(dir).rglob(suffix)])
    return paths
