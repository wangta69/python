from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QMessageBox
from PyQt5.QtCore import QRect

class MyInfoWindow(QWidget):

    def __init__(self, kiwoom=None):
        super().__init__()


        self.kiwoom = kiwoom
        self.isLogin = kiwoom.dynamicCall("GetConnectState()")

        if self.isLogin != 1:
            QMessageBox.about(self, 'Alert', "먼저 로그인 해 주세요")
        else:
            self.user_name = kiwoom.get_login_info("USER_NAME")
            self.user_id = kiwoom.get_login_info("USER_ID")
            self.account_count = kiwoom.get_login_info("ACCOUNT_CNT")
            account_list = kiwoom.get_login_info("ACCNO")
            self.account_number = account_list.split(';')[0]

            print(self.user_name, self.user_id, self.account_count, self.account_number)
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

