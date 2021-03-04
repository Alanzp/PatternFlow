import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap

from mainView import Ui_MainWindow
import cv2
import numpy as np
from pathlib import Path
import processImageClasses
import matplotlib.pyplot as plt
import inspect


# To solve cv2 can not read path contain Chinese words
def cv_imread(file_path):
    img = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), -1)
    return img


class PyQtMainEntry(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(PyQtMainEntry, self).__init__(parent)
        self.setupUi(self)
        self.InputFreezeFlag = False
        self.autoProcessImage = False
        self.loadProcessClass()
        self.timer = QTimer()
        # Set window reflash FPS during open camera
        self.FPS = 40
        self.timer.setInterval(1000 // self.FPS)
        # Bind menu action
        self.actionOpen_File.triggered.connect(self.OpenFile)
        self.actionOpen_Dirs.triggered.connect(self.OpenDir)
        self.actionOpen_Carmera.triggered.connect(self.OpenCarmera)

    def loadProcessClass(self):
        self.workClasses = dict(
            inspect.getmembers(processImageClasses, inspect.isclass))
        for clss in self.workClasses.keys():
            action = QtWidgets.QAction(self)
            action.setText(clss)
            action.setObjectName(clss)
            action.triggered.connect(self.ChangeClass)
            self.menu_4.addAction(action)
        self.ImageWorker = self.workClasses[clss]()
        self.processMethod = self.ImageWorker.process
        self.args = self.ImageWorker.args
        self.groupBox_5.setTitle(clss)
        self.InitArgsField()

    def ChangeClass(self):
        sender = self.sender()
        self.ImageWorker = self.workClasses[sender.objectName()]()
        self.processMethod = self.ImageWorker.process
        self.args = self.ImageWorker.args
        self.groupBox_5.setTitle(sender.objectName())
        self.InitArgsField()

    def InitArgsField(self):
        group = self.groupBox_5
        gridLayout = self.groupBox_5.layout()
        if self.gridLayout.count() > 0:
            for item in group.children()[1:]:
                item.deleteLater()
        QApplication.processEvents()
        MaxCol = 6
        row = 0
        col = 0
        for i, argName in enumerate(self.args.keys()):
            QLayout = QtWidgets.QHBoxLayout()
            Label = QtWidgets.QLabel(group)
            Label.setText(argName + "(%)")
            QLayout.addWidget(Label)
            if type(self.args[argName][1]) == tuple:
                spinBox = QtWidgets.QSpinBox(group)
                spinBox.setObjectName(argName)
                spinBox.setValue(self.args[argName][0])
                spinBox.setMinimum(self.args[argName][1][0])
                spinBox.setMaximum(self.args[argName][1][1])
                spinBox.valueChanged.connect(self.SpinValueChange)
                QLayout.addWidget(spinBox)
            row = i // MaxCol
            col = i % MaxCol
            gridLayout.addLayout(QLayout, row, col, 1, 1)

    def SpinValueChange(self, value):
        sender = self.sender()
        self.args[sender.objectName()][0] = value
        if self.autoProcessImage:
            self.processImage()

    def OpenFile(self):
        fileName, filetype = QFileDialog.getOpenFileName(
            self, "选取文件", "./",
            "IMAGE Files (*.png;*.jpg;" + "*jpe;*jpeg:*bmp);; All Files (*)")
        # 设置文件扩展名过滤,注意用双分号间隔
        if not fileName:
            return
        print(fileName, filetype)
        self.listWidget.clear()
        self.filePath = Path(fileName)
        self.inputDir = self.filePath.parent
        self.listWidget.addItem(self.filePath.name)
        self.listWidget.itemAt(0, 0).setSelected(True)

    def OpenDir(self):
        directory = QFileDialog.getExistingDirectory(self, "选取文件夹", r"./")
        print(directory)
        self.listWidget.clear()
        if not directory:
            return
        self.inputDir = directory
        self.imagePaths = []
        for suffix in ["*.jpg", "*.png", "*.jpeg", "*.bmp", "*.jpe"]:
            self.imagePaths.extend(
                [path for path in Path(directory).rglob(suffix)])
        print(self.imagePaths)
        for item in self.imagePaths:
            self.listWidget.addItem(str(item.relative_to(self.inputDir)))
        self.listWidget.itemAt(0, 0).setSelected(True)

    def OpenCarmera(self):
        self.listWidget.clear()
        self.cap = cv2.VideoCapture(0)
        self.timer.start()
        self.timer.timeout.connect(self.capture)

    def capture(self):
        if self.cap.isOpened():
            # Get one frame
            ret, img = self.cap.read()
            img = cv2.flip(img, 1)
            self.filePath = Path("./").joinpath("capture")
            self.inputImage_BGR = img
            self.inputImage_RBG = cv2.cvtColor(self.inputImage_BGR,
                                               cv2.COLOR_BGR2RGB)
            self.showInputImage()

    def closeCapture(self):
        if not hasattr(self, "cap"):
            return
        if not hasattr(self, "timer"):
            return
        self.cap.release()
        self.timer.stop()

    def freezeInput(self):
        if self.InputFreezeFlag:
            self.pushButton_7.setText("Freeze")
            self.InputFreezeFlag = False
            self.label.setStyleSheet("")
        else:
            self.pushButton_7.setText("Unfreeze")
            self.InputFreezeFlag = True
            self.label.setStyleSheet('background-color: rgb(255, 0, 0)')

    def processImage(self):
        if not hasattr(self, "inputImage_BGR"):
            return
        self.outputImage_BGR = self.processMethod(self.inputImage_BGR)
        self.outputImage_RGB = cv2.cvtColor(self.outputImage_BGR,
                                            cv2.COLOR_BGR2RGB)
        self.label_4.setText(self.ImageWorker.outputStr())
        self.showOutputImage()

    def doSave(self, fileName, imageSave):
        saveRoot = self.label_6.text()
        saveRoot = Path(saveRoot)
        print(saveRoot.joinpath(fileName))
        plt.imsave(saveRoot.joinpath(fileName), imageSave)

    def saveImage(self):
        self.doSave(self.filePath.name, self.outputImage_RGB)

    def changeSaveDir(self):
        directory = QFileDialog.getExistingDirectory(self, "选取文件夹",
                                                     self.label_6.text())
        print(directory)
        self.label_6.setText(directory)

    def saveAllImage(self):
        filesCount = len(self.imagePaths)
        saveRoot = self.label_6.text()
        saveRoot = Path(saveRoot)
        for index, path in enumerate(self.imagePaths):
            raletivePath = path.relative_to(self.inputDir)
            img = cv_imread(path)
            img = self.processMethod(img)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            saveDir = saveRoot.joinpath(raletivePath).parent
            if not saveDir.exists():
                saveDir.mkdir(parents=True)
            self.doSave(fileName=raletivePath, imageSave=img)
            print("已完成{:.2f}%".format((index + 1) / filesCount * 100))

    def setProcessAuto(self):
        if self.autoProcessImage:
            self.autoProcessImage = False
        else:
            self.autoProcessImage = True

    def resizeEvent(self, event):
        self.showInputImage()

    def loadImage(self):
        if not hasattr(self, "inputDir"):
            return
        ls = self.listWidget.selectedIndexes()
        if len(ls) == 0:
            return
        self.filePath = Path(self.inputDir).joinpath(ls[0].data())
        self.inputImage_BGR = cv_imread(str(self.filePath))
        self.inputImage_RBG = cv2.cvtColor(self.inputImage_BGR,
                                           cv2.COLOR_BGR2RGB)
        self.showInputImage()

    def showInputImage(self):
        if self.InputFreezeFlag:
            return
        if not hasattr(self, "inputImage_RBG"):
            return
        rows, cols, channels = self.inputImage_RBG.shape
        bytesPerLine = channels * cols
        QImg = QImage(self.inputImage_RBG.data, cols, rows, bytesPerLine,
                      QImage.Format_RGB888)
        QImg = QImg.scaled(self.label.size(), Qt.KeepAspectRatio,
                           Qt.SmoothTransformation)
        self.label.setPixmap(QPixmap.fromImage(QImg))
        self.label_3.setText(self.filePath.name)
        if self.autoProcessImage:
            self.processImage()

    def showOutputImage(self):
        if not hasattr(self, "outputImage_RGB"):
            return
        rows, cols, channels = self.outputImage_RGB.shape
        bytesPerLine = channels * cols
        QImg = QImage(self.outputImage_RGB.data, cols, rows, bytesPerLine,
                      QImage.Format_RGB888)
        QImg = QImg.scaled(self.label_2.size(), Qt.KeepAspectRatio,
                           Qt.SmoothTransformation)
        self.label_2.setPixmap(QPixmap.fromImage(QImg))
        QApplication.processEvents()


def calResize(QsizeIn, QsizeOut):
    gapH = QsizeIn.height() - QsizeOut.height()
    gapW = QsizeIn.width() - QsizeOut.width()
    if gapH > gapW:
        H = QsizeOut.height()
        W = H * QsizeIn.width() // QsizeIn.height()
    else:
        W = QsizeOut.width()
        H = W * QsizeIn.height() // QsizeIn.width()
    return QtCore.QSize(W, H)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = PyQtMainEntry()
    myWin.show()
    sys.exit(app.exec_())
