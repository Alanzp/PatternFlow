import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap

from mainView import Ui_MainWindow
from pathlib import Path
import processer
from load.camera import Camera
from util.thread import MyThread
from load.file import importImageFile, getImagePaths
from util.image import convertBGR2RGB, imageFormatForShow
from export.localFile import doSaveLocalFile, genCaptureFileName


class PyQtMainEntry(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(PyQtMainEntry, self).__init__(parent)
        self.setupUi(self)
        self.InputFreezeFlag = False
        self.autoProcessImage = False
        self.loadProcessClass()
        self.timer = QTimer()
        # Set window reflash FPS during open camera
        self.FPS = 20
        self.timer.setInterval(1000 // self.FPS)
        # Bind menu action
        self.actionOpen_File.triggered.connect(self.OpenFile)
        self.actionOpen_Dirs.triggered.connect(self.OpenDir)
        self.actionOpen_Carmera.triggered.connect(self.OpenCarmera)

    def loadProcessClass(self):
        self.workClasses = {clss.__name__: clss for clss in processer.__all__}
        for clss in self.workClasses.keys():
            action = QtWidgets.QAction(self)
            action.setText(clss)
            action.setObjectName(clss)
            action.triggered.connect(self.ChangeClass)
            self.menu_4.addAction(action)
        self.ImageWorker = self.workClasses[clss]()
        self.processMethod = self.ImageWorker.process
        self.args = self.ImageWorker.params
        self.groupBox_5.setTitle(clss)
        self.InitArgsField()

    def ChangeClass(self):
        sender = self.sender()
        self.ImageWorker = self.workClasses[sender.objectName()]()
        self.processMethod = self.ImageWorker.process
        self.args = self.ImageWorker.params
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
            spinBox = QtWidgets.QSpinBox(group)
            spinBox.setObjectName(argName)
            spinBox.setValue(self.args[argName].getCurrent())
            spinBox.setMinimum(self.args[argName].getMin())
            spinBox.setMaximum(self.args[argName].getMax())
            spinBox.valueChanged.connect(self.SpinValueChange)
            QLayout.addWidget(spinBox)
            row = i // MaxCol
            col = i % MaxCol
            gridLayout.addLayout(QLayout, row, col, 1, 1)

    def SpinValueChange(self, value):
        sender = self.sender()
        self.args[sender.objectName()].setCurrent(value)
        if self.autoProcessImage:
            self.processImage()

    def OpenFile(self):
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Select File", "./",
            "IMAGE Files (*.png;*.jpg;" + "*jpe;*jpeg:*bmp);; All Files (*)")
        if not fileName:
            return
        self.listWidget.clear()
        self.filePath = Path(fileName)
        self.inputDir = self.filePath.parent
        self.listWidget.addItem(self.filePath.name)
        self.listWidget.itemAt(0, 0).setSelected(True)

    def OpenDir(self):
        directory = QFileDialog.getExistingDirectory(self, "Select directory", r"./")
        self.listWidget.clear()
        if not directory:
            return
        self.inputDir = directory
        self.imagePaths = getImagePaths(directory)
        if len(self.imagePaths) == 0:
            return
        for item in self.imagePaths:
            self.listWidget.addItem(str(item.relative_to(self.inputDir)))
        self.listWidget.itemAt(0, 0).setSelected(True)

    def OpenCarmera(self):
        self.listWidget.clear()
        self.cap = Camera()
        self.timer.start()
        self.timer.timeout.connect(self.capture)

    def capture(self):
        img = self.cap.getCurrentFrame()
        if img is not None:
            self.filePath = Path("./").joinpath(genCaptureFileName())
            self.inputImage_BGR = img
            self.inputImage_RBG = convertBGR2RGB(img)
            self.showInputImage()

    def closeCapture(self):
        if not hasattr(self, "cap"):
            return
        if not hasattr(self, "timer"):
            return
        self.cap.closeCamera()
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
        if hasattr(self, "worker") and self.worker.isRunning():
            return
        self.worker = MyThread(self.processMethod, self.inputImage_BGR)
        self.worker.sinOut.connect(self.showOutputImage)
        self.worker.start()
        self.label_4.setText(
            self.ImageWorker.outputStr() +
            "|process time cost(ms):{:.2f}".format(MyThread.timeCost))

    def saveImage(self):
        doSaveLocalFile(self.label_6.text(), self.filePath.name,
                        self.outputImage_RGB)

    def changeSaveDir(self):
        directory = QFileDialog.getExistingDirectory(self, "Select directory",
                                                     self.label_6.text())
        self.label_6.setText(directory)

    def saveAllImage(self):
        filesCount = len(self.imagePaths)
        saveRoot = Path(self.label_6.text())
        for index, path in enumerate(self.imagePaths):
            raletivePath = path.relative_to(self.inputDir)
            img = importImageFile(path)
            img = self.processMethod(img)
            img = convertBGR2RGB(img)
            saveDir = saveRoot.joinpath(raletivePath).parent
            if not saveDir.exists():
                saveDir.mkdir(parents=True)
            doSaveLocalFile(self.label_6.text(),
                            fileName=raletivePath,
                            imageSave=img)
            print("complete {:.2f}%".format((index + 1) / filesCount * 100))

    def setProcessAuto(self):
        if self.autoProcessImage:
            self.autoProcessImage = False
        else:
            self.autoProcessImage = True

    def loadImage(self):
        if not hasattr(self, "inputDir"):
            return
        ls = self.listWidget.selectedIndexes()
        if len(ls) == 0:
            return
        self.filePath = Path(self.inputDir).joinpath(ls[0].data())
        self.inputImage_BGR = importImageFile(str(self.filePath))
        self.inputImage_RBG = convertBGR2RGB(self.inputImage_BGR)
        self.showInputImage()

    def showInputImage(self):
        if self.InputFreezeFlag:
            return
        if not hasattr(self, "inputImage_RBG"):
            return
        QImg = imageFormatForShow(self.inputImage_RBG, self.label.size())
        self.label.setPixmap(QPixmap.fromImage(QImg))
        self.label_3.setText(self.filePath.name)
        if self.autoProcessImage:
            self.processImage()

    def showOutputImage(self, image):
        if not hasattr(self, "worker"):
            return
        if not hasattr(self.worker, "outputImg"):
            return
        self.outputImage_BGR = image
        self.outputImage_RGB = convertBGR2RGB(image)
        if not hasattr(self, "outputImage_RGB"):
            return
        QImg = imageFormatForShow(self.outputImage_RGB, self.label_2.size())
        self.label_2.setPixmap(QPixmap.fromImage(QImg))
        QApplication.processEvents()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = PyQtMainEntry()
    myWin.show()
    sys.exit(app.exec_())
