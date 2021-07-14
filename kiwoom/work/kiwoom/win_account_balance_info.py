from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QMessageBox
from PyQt5.QtCore import QRect
from PyQt5 import uic

form_class = uic.loadUiType("ui/kiwoom/win_account_balance_info.ui")[0]

class AccountBalanceInfoWindow(QWidget):

    def __init__(self, kiwoom=None):
        super().__init__()
        self.kiwoom = kiwoom
        self.setupUi(self)  # 현재 form_class를 선택한다.

        self.isLogin = kiwoom.is_login()

        if self.isLogin != 1:
            QMessageBox.about(self, 'Alert', "먼저 로그인 해 주세요")
        else:
            self.get_account_info()
            self.kiwoom.comm_rq_data("계좌평가잔고내역요청", "opw00018", 0, 10)
            self.labelBuyAmt.setText(str(self.kiwoom.total_buy_money) + '원') # 총 매입 금액
            self.labelEvaluAmt.setText(str(self.kiwoom.total_evaluation_money) + '원') # 총 평가 금액
            self.labelProfitLoss.setText(str(self.kiwoom.total_evaluation_profit_and_loss_money) + '원') # 총 평가 손익 금액
            self.labelTotalYield.setText(str(self.kiwoom.total_yield) + '원') # 총 수익률


    def get_account_number(self):
        account_list = self.kiwoom.get_login_info("ACCNO")
        account_number = account_list.split(';')[0]
        self.account_number = account_number

            # lBuy = QLabel('총 매입 금액: ' + str(self.kiwoom.total_buy_money) + '원', self)
            # lBuy.setGeometry(QRect(20, 40, 400, 20))
            #
            # lEvalu = QLabel('총 평가 금액: ' + str(self.kiwoom.total_evaluation_money) + '원', self)
            # # lEvalu.move(20, 80)
            # lEvalu.setGeometry(QRect(20, 60, 400, 20))
            #
            # lProfitLoss = QLabel('총 평가 손익 금액: ' + str(self.kiwoom.total_evaluation_profit_and_loss_money) + '원', self)
            # # lProfitLoss.move(20, 80)
            # lProfitLoss.setGeometry(QRect(20, 80, 400, 20))
            #
            # lYield = QLabel('총 수익률: ' + str(self.kiwoom.total_yield) + '원', self)
            # # lYield.move(20, 80)
            # lYield.setGeometry(QRect(20, 100, 400, 20))

    #
    #
    #
    #
    # def initUI(self):
    #     okButton = QPushButton('OK')
    #     okButton.clicked.connect(self.close)
    #
    #     hbox = QHBoxLayout()
    #     hbox.addStretch(1)
    #     hbox.addWidget(okButton)
    #     hbox.addStretch(1)
    #
    #     vbox = QVBoxLayout()
    #     vbox.addStretch(3)
    #     vbox.addLayout(hbox)
    #     vbox.addStretch(1)
    #
    #
    #     self.setLayout(vbox)
    #
    #     self.setWindowTitle('Login State')
    #     self.setGeometry(300, 300, 300, 200)
    #
    #     # os.system('cls')
    #     # print("\n<싱글 데이터>")
    #     # print(f"총 매입 금액 : {self.total_buy_money}원")
    #     # print(f"총 평가 금액 : {self.total_evaluation_money}원")
    #     # print(f"총 평가 손익 금액 : {self.total_evaluation_profit_and_loss_money}원")
    #     # print(f"총 수익률 : {self.total_yield}%\n")
    #     #
    #     # table = self.make_table("계좌평가잔고내역요청")
    #     # print("<멀티 데이터>")
    #     # if len(self.account_stock_dict) == 0:
    #     #     print("보유한 종목이 없습니다!")
    #     # else:
    #     #     print(f"보유 종목 수 : {len(self.account_stock_dict)}개")
    #     #     print(table)
    #     # input()
    #
    #     lBuy = QLabel('총 매입 금액: ' + str(self.kiwoom.total_buy_money) + '원', self)
    #     lBuy.setGeometry(QRect(20, 40, 400, 20))
    #
    #     lEvalu = QLabel('총 평가 금액: ' + str(self.kiwoom.total_evaluation_money) + '원', self)
    #     # lEvalu.move(20, 80)
    #     lEvalu.setGeometry(QRect(20, 60, 400, 20))
    #
    #     lProfitLoss = QLabel('총 평가 손익 금액: ' + str(self.kiwoom.total_evaluation_profit_and_loss_money) + '원', self)
    #     # lProfitLoss.move(20, 80)
    #     lProfitLoss.setGeometry(QRect(20, 80, 400, 20))
    #
    #     lYield = QLabel('총 수익률: ' + str(self.kiwoom.total_yield) + '원', self)
    #     # lYield.move(20, 80)
    #     lYield.setGeometry(QRect(20, 100, 400, 20))
    #


    # ## 평가잔고내역 조회
    # def get_account_evaluation_balance(self, nPrevNext=0):
    #     self.set_input_value("계좌번호", self.account_number)
    #     self.set_input_value("비밀번호", " ")
    #     self.set_input_value("비밀번호입력매체구분", "00")
    #     self.set_input_value("조회구분", "1")
    #     self.comm_rq_data("계좌평가잔고내역요청", "opw00018", nPrevNext, self.screen_my_account)
    #
    #     if not self.account_event_loop.isRunning():
    #         self.account_event_loop.exec_()