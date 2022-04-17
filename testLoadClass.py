import inspect
import processer


if __name__ == "__main__":
    print(inspect.getmembers(processer, inspect.ismodule))
    # self.workClasses = dict(
    #         inspect.getmembers(processer, inspect.isclass))
    # for clss in self.workClasses.keys():
    #     action = QtWidgets.QAction(self)
    #     action.setText(clss)
    #     action.setObjectName(clss)
    #     action.triggered.connect(self.ChangeClass)
    #     self.menu_4.addAction(action)
    # self.ImageWorker = self.workClasses[clss]()
    # self.processMethod = self.ImageWorker.process
    # self.args = self.ImageWorker.args
    # self.groupBox_5.setTitle(clss)
    # self.InitArgsField()
