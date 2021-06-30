from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtCore import QRect

class AccountBalanceInfoWindow(QWidget):

    def __init__(self, parent=None):
        super().__init__()
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

        # os.system('cls')
        # print("\n<싱글 데이터>")
        # print(f"총 매입 금액 : {self.total_buy_money}원")
        # print(f"총 평가 금액 : {self.total_evaluation_money}원")
        # print(f"총 평가 손익 금액 : {self.total_evaluation_profit_and_loss_money}원")
        # print(f"총 수익률 : {self.total_yield}%\n")
        #
        # table = self.make_table("계좌평가잔고내역요청")
        # print("<멀티 데이터>")
        # if len(self.account_stock_dict) == 0:
        #     print("보유한 종목이 없습니다!")
        # else:
        #     print(f"보유 종목 수 : {len(self.account_stock_dict)}개")
        #     print(table)
        # input()

        lBuy = QLabel('총 매입 금액: ' + str(self.parent.total_buy_money) + '원', self)
        lBuy.setGeometry(QRect(20, 40, 400, 20))

        lEvalu = QLabel('총 평가 금액: ' + str(self.parent.total_evaluation_money) + '원', self)
        # lEvalu.move(20, 80)
        lEvalu.setGeometry(QRect(20, 60, 400, 20))

        lProfitLoss = QLabel('총 평가 손익 금액: ' + str(self.parent.total_evaluation_profit_and_loss_money) + '원', self)
        # lProfitLoss.move(20, 80)
        lProfitLoss.setGeometry(QRect(20, 80, 400, 20))

        lYield = QLabel('총 수익률: ' + str(self.parent.total_yield) + '원', self)
        # lYield.move(20, 80)
        lYield.setGeometry(QRect(20, 100, 400, 20))