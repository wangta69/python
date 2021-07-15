from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5 import uic
from collections import deque

form_class = uic.loadUiType("ui/kiwoom/win_account_balance_info.ui")[0]

class AccountBalanceInfoWindow(QWidget, form_class):

    def __init__(self, kiwoom=None):
        super().__init__()
        self.kiwoom = kiwoom
        self.setupUi(self)  # 현재 form_class를 선택한다.

        self.isLogin = kiwoom.is_login()

        # ComboBox에 기능 연결
        self.comboAccount.currentIndexChanged.connect(self.comboBoxFunction)

        if self.isLogin != 1:
            QMessageBox.about(self, 'Alert', "먼저 로그인 해 주세요")
        else:
            self.get_account_number()

    def get_account_number(self):
        accounts_list = self.kiwoom.get_login_info("ACCNO")
        accounts = deque(accounts_list.split(';'))
        accounts.appendleft('== 선택 ==')
        self.comboAccount.addItems(accounts)

    def comboBoxFunction(self):
        account_number = self.comboAccount.currentText()
        if account_number != '== 선택 ==':
            self.kiwoom.get_account_evaluation_balance(account_number, 0, 10)
            # self.kiwoom.comm_rq_data("계좌평가잔고내역요청", "opw00018", 0, 10)
            self.labelBuyAmt.setText(str(self.kiwoom.total_buy_money) + '원')  # 총 매입 금액
            self.labelEvaluAmt.setText(str(self.kiwoom.total_evaluation_money) + '원')  # 총 평가 금액
            self.labelProfitLoss.setText(str(self.kiwoom.total_evaluation_profit_and_loss_money) + '원')  # 총 평가 손익 금액
            self.labelTotalYield.setText(str(self.kiwoom.total_yield) + '원')  # 총 수익률
