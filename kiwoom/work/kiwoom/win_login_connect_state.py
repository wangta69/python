from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtCore import QRect

class LoginConnectStateWindow(QWidget):

    def __init__(self, parent=None):
        super().__init__()
        self.isLogin = parent.dynamicCall("GetConnectState()")
        self.initUI()

    def initUI(self):
        okButton = QPushButton('OK')
        okButton.clicked.connect(self.close)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(okButton)
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(3)
        vbox.addLayout(hbox)
        vbox.addStretch(1)


        self.setLayout(vbox)

        self.setWindowTitle('Login State')
        self.setGeometry(300, 300, 300, 200)

        label = QLabel('', self)
        # label.move(20, 20)
        label.setGeometry(QRect(20, 20, 200, 31))
        if self.isLogin == 1:
             label.setText('현재 계정은 로그인 상태입니다')
        else:
             label.setText('현재 계정은 로그아웃 상태입니다.')
