import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class Worker(QObject):
    user_signal = pyqtSignal()

    def run(self):
        self.user_signal.emit()

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        worker = Worker()
        worker.user_signal.connect(self.user_slot)
        worker.run()

    @pyqtSlot()
    def user_slot(self):
        print("user slot")

app = QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec_()