from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5 import uic
from collections import deque

form_class = uic.loadUiType("ui/kiwoom/win_deposit_info.ui")[0]

class DepositInfoWindow(QWidget, form_class):

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
            self.kiwoom.get_deposit_info(account_number, 0, 11)

            self.labelDepositAmt.setText(str(self.kiwoom.deposit) + '원')  # 예수금
            self.labelAvailWithDrawAmt.setText(str(self.kiwoom.withdraw_deposit) + '원')  # 출금 가능 금액
            self.labelAvailOrderAmt.setText(str(self.kiwoom.order_deposit) + '원')  # 주문 가능 금액

    #
    #     lDeposit= QLabel('예수금: ' + str(self.kiwoom.deposit) + '원', self)
    #     lDeposit.setGeometry(QRect(20, 40, 400, 20))
    #
    #     lWithdraw = QLabel('출금 가능 금액: ' + str(self.kiwoom.withdraw_deposit) + '원', self)
    #     # lWithdraw.move(20, 80)
    #     lWithdraw.setGeometry(QRect(20, 60, 400, 20))
    #
    #     lOrder = QLabel('주문 가능 금액: ' + str(self.kiwoom.order_deposit) + '원', self)
    #     # lOrder.move(20, 80)
    #     lOrder.setGeometry(QRect(20, 80, 400, 20))

