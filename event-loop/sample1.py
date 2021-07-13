import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QTimer, QEventLoop


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.local_event_loop = QEventLoop()
        self.timer = QTimer(self)
        self.timer.singleShot(1000, self.login_callback)
        self.local_event_loop.exec()            # 이 라인에서 self.local_event_loop가 quit될 때까지 대기 (이벤트는 처리됨)
        self.check_balance()

    def login_callback(self):
        self.balance = 100
        self.local_event_loop.exit()

    def check_balance(self):
        print(self.balance)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()     # main event loop