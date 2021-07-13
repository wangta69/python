import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import time


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.event_loop = QEventLoop()

        btn1 = QPushButton("button1", self)
        btn1.move(10, 10)
        btn1.clicked.connect(self.btn1_clicked)

        btn2 = QPushButton("button2", self)
        btn2.move(10, 40)
        btn2.clicked.connect(self.btn2_clicked)

        btn3 = QPushButton("button3", self)
        btn3.move(10, 70)
        btn3.clicked.connect(self.btn3_clicked)

    def btn1_clicked(self):
        print("before1 loop exec")  #1 번출력
        self.event_loop.exec_() # 이 구문이하는 event_loop.exit()를 만나기 전까지는 실행되지 않는다.
        print("after1 loop exec") # 5번 출력

    def btn2_clicked(self):
        print("before2 loop exit") # 2번 출력
        self.event_loop.exit()
        print("after2 loop exit") # 3번출력
        time.sleep(5)
        print("after2 time sleep") # 4번 출력

    def btn3_clicked(self):
        print("button3 clicked event")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()