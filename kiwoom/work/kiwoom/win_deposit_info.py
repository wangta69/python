from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtCore import QRect

class DepositInfoWindow(QWidget):

    def __init__(self, parent=None):
        super().__init__()
        # parent.get_deposit_info()
        # print(f"\n예수금 : {parent.deposit}원")
        # print(f"출금 가능 금액 : {parent.withdraw_deposit}원")
        # print(f"주문 가능 금액 : {parent.order_deposit}원")
        self.parent = parent
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


        lDeposit= QLabel('예수금: ' + str(self.parent.deposit) + '원', self)
        lDeposit.setGeometry(QRect(20, 40, 400, 20))

        lWithdraw = QLabel('출금 가능 금액: ' + str(self.parent.withdraw_deposit) + '원', self)
        # lWithdraw.move(20, 80)
        lWithdraw.setGeometry(QRect(20, 60, 400, 20))

        lOrder = QLabel('주문 가능 금액: ' + str(self.parent.order_deposit) + '원', self)
        # lOrder.move(20, 80)
        lOrder.setGeometry(QRect(20, 80, 400, 20))

