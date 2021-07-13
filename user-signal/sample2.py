import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


class Worker(QObject):
    user_signal = pyqtSignal(int, int)

    def run(self):
        self.user_signal.emit(1, 2)


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        worker = Worker()
        worker.user_signal.connect(self.user_slot)
        worker.run()

    @pyqtSlot(int, int)
    def user_slot(self, arg1, arg2):
        print(arg1, arg2)


app = QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec_()