from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtCore import QRect

class MyInfoWindow(QWidget):

    def __init__(self, parent=None):
        super().__init__()

        self.user_name = parent.dynamicCall("GetLoginInfo(QString)", "USER_NAME")
        self.user_id = parent.dynamicCall("GetLoginInfo(QString)", "USER_ID")
        self.account_count = parent.dynamicCall("GetLoginInfo(QString)", "ACCOUNT_CNT")
        account_list = parent.dynamicCall("GetLoginInfo(QString)", "ACCNO")
        self.account_number = account_list.split(';')[0]
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
        self.setWindowTitle('My Infomation')
        self.setGeometry(300, 300, 300, 200)

        lName = QLabel('이름: ' + self.user_name, self)
        lName.move(20, 20)

        lName = QLabel('아이디: ' + self.user_id, self)
        lName.move(20, 40)

        lName = QLabel('계좌수: ' + self.account_count, self)
        lName.move(20, 60)

        lName = QLabel('계좌번호: ' + self.account_number, self)
        # lName.move(20, 80)
        lName.setGeometry(QRect(20, 80, 400, 20))

