from PyQt5.QtWidgets import QWidget, QMessageBox, QTableWidgetItem
from PyQt5 import uic
from PyQt5.QtCore import QEventLoop, Qt

import time
from kiwoom.worker import Worker

form_class = uic.loadUiType("ui/kiwoom/main.ui")[0]

# referer : https://wikidocs.net/

class OrderWindow(QWidget, form_class):

    def __init__(self, kiwoom=None):
        super().__init__()
        self.kiwoom = kiwoom
        self.setupUi(self)  # 현재 form_class를 선택한다.

        self.lineEdit.textChanged.connect(self.code_changed)

        self.isLogin = kiwoom.is_login()
        if self.isLogin != 1:
            QMessageBox.about(self, 'Alert', "먼저 로그인 해 주세요")
            pass
        else:
            self.set_account_combo()
            
            # 주문
            self.pushButtonSetOrder.clicked.connect(self.send_order)
            # 조회
            self.buttonCheckBalance.clicked.connect(self.check_balance)

            # 이벤트 루프 관련 변수
            self.tr_event_loop = QEventLoop()

            self.worker = Worker()
            self.worker.signal_on_receive_tr_data.connect(self.signal_tr_data)
            self.kiwoom.OnReceiveTrData.connect(self.signal_tr_data)

            # table 관련
            self.tableMyItems.setSortingEnabled(True)

    def signal_tr_data(self, src_no, rq_name, tr_code, record_name, prev_next):
        pass

    def set_account_combo(self):
        """
        계좌를 combo box에 리스트 한다.
        :return:
        """
        accouns_num = int(self.kiwoom.get_login_info("ACCOUNT_CNT"))
        accounts = self.kiwoom.get_login_info("ACCNO")
        accounts_list = accounts.split(';')[0:accouns_num]
        self.comboAccount.addItems(accounts_list)


    # def send_order(self, rqname, screen_no, acc_no, order_type, code, quantity, price, hoga, order_no):
    def send_order(self):
        rqname = 'send_order_req'
        screen_no = '0101'
        order_type_lookup = {'신규매수': 1, '신규매도': 2, '매수취소': 3, '매도취소': 4}
        hoga_lookup = {'지정가': "00", '시장가': "03"}
        hoga = self.comboHoga.currentText()

        acc_no = self.comboAccount.currentText()
        order_type_str = self.comboOrderType.currentText()
        order_type = order_type_lookup[order_type_str]
        code = self.lineEdit.text()

        quantity = self.spinQuantity.value()
        price = self.spinBoxPrice.value()
        order_no = hoga_lookup[hoga]
        pass
        self.kiwoom.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)",
                         [rqname, screen_no, acc_no, order_type, code, quantity, price, hoga, order_no])

    # def get_chejan_data(self, fid):
    #     ret = self.kiwoom.get_chejan_data(fid)
    #     return ret

    def code_changed(self):
        code = self.lineEdit.text()
        name = self.kiwoom.get_master_code_name(code)
        self.lineEdit_2.setText(name)

    def reset_opw00018_output(self):
        self.opw00018_output = {'single': [], 'multi': []}

    def check_balance(self):
        self.reset_opw00018_output()
        self.kiwoom.account_number = self.comboAccount.currentText()
        print('[check_balance] start')
        self.kiwoom.get_account_evaluation_balance(self.kiwoom.account_number, 0, "2000")
        self.kiwoom.get_deposit_info(self.kiwoom.account_number, 0, "2000")
        print('[check_balance] end')
        self.set_evaulation_balance()
        self.set_table_my_items(self.kiwoom.account_stock_dict)

        # # account_number = self.kiwoom.get_login_info("ACCNO")
        # self.kiwoom.account_number = self.comboAccount.currentText()
        # print('check_balance > account_number', self.kiwoom.account_number)
        #
        # self.kiwoom.set_input_value("계좌번호", self.kiwoom.account_number)
        # self.kiwoom.comm_rq_data("계좌평가잔고내역요청", "opw00018", 0, "2000")
        # self.tr_event_loop.exec_()

        #
        # while self.kiwoom.remained_data:
        #     print('self.kiwoom.remained_data')
        #     time.sleep(0.2)
        #     self.kiwoom.get_account_evaluation_balance(self.kiwoom.account_number, 2, "2000")
        #     # self.kiwoom.set_input_value("계좌번호", self.kiwoom.account_number)
        #     # self.kiwoom.comm_rq_data("계좌평가잔고내역요청", "opw00018", 2, "2000")

    def set_table_my_items(self, account_stocks):
        """
        보유종목 현황
        :param account_stocks:
        :return:
        """
        self.tableMyItems.setRowCount(len(account_stocks))
        count = 0
        for key in account_stocks:
            # print(row[0], row[1], row[2], row[3])
            self.tableMyItems.setItem(count, 0, QTableWidgetItem(str(account_stocks[key]['종목명'])))
            # self.tableMyItems.setItem(count, 1, QTableWidgetItem(str(account_stocks[key]['보유수량'])))

            보유수량 = QTableWidgetItem()
            보유수량.setData(Qt.DisplayRole, account_stocks[key]['보유수량'])
            self.tableMyItems.setItem(count, 1, 보유수량)
            # self.tableMyItems.setItem(count, 1, QTableWidgetItem(str(account_stocks[key]['보유수량'])))

            self.tableMyItems.setItem(count, 2, QTableWidgetItem(str(account_stocks[key]['매입가'])))
            self.tableMyItems.setItem(count, 3, QTableWidgetItem(str(account_stocks[key]['현재가'])))

            평가손익 = QTableWidgetItem()
            평가손익.setData(Qt.DisplayRole, account_stocks[key]['평가손익'])
            self.tableMyItems.setItem(count, 4, 평가손익)
            # self.tableMyItems.setItem(count, 4, QTableWidgetItem(str(account_stocks[key]['평가손익'])))
            self.tableMyItems.setItem(count, 5, QTableWidgetItem(str(account_stocks[key]['수익률(%)'])))
            self.tableMyItems.item(count, 1).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tableMyItems.item(count, 2).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tableMyItems.item(count, 3).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tableMyItems.item(count, 4).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tableMyItems.item(count, 5).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

            # self.tableMyItems.setItem(count, 4, QTableWidgetItem(row[4].strftime('%d/%m/%Y %H:%M:%S')))
            count += 1

        self.tableMyItems.sortItems(4, Qt.AscendingOrder)

    # def sort(self, Ncol, order):
    #     print("sort", Ncol, order)
    #     """Sort table by given column number."""
    #     self.layoutAboutToBeChanged.emit()
    #     self.data = self.data.sort_values(self.headers[Ncol],
    #                                       ascending=order == Qt.AscendingOrder)
    #     self.layoutChanged.emit()

    def set_evaulation_balance(self):
        """
        잔고
        :return: 
        """
        self.tableEvaulaltion.setRowCount(1)
        self.tableEvaulaltion.setItem(0, 0, QTableWidgetItem(str(self.kiwoom.opw00001Data['d+2추정예수금'])))
        self.tableEvaulaltion.setItem(0, 1, QTableWidgetItem(str(self.kiwoom.opw00018Data['accountEvaluation']['총매입금액'])))
        self.tableEvaulaltion.setItem(0, 2, QTableWidgetItem(str(self.kiwoom.opw00018Data['accountEvaluation']['총평가금액'])))
        self.tableEvaulaltion.setItem(0, 3, QTableWidgetItem(str(self.kiwoom.opw00018Data['accountEvaluation']['총평가손익금액'])))
        self.tableEvaulaltion.setItem(0, 4, QTableWidgetItem(str(self.kiwoom.opw00018Data['accountEvaluation']['총수익률(%)'])))
        self.tableEvaulaltion.setItem(0, 5, QTableWidgetItem(str(self.kiwoom.opw00018Data['accountEvaluation']['추정예탁자산'])))
        self.tableEvaulaltion.item(0, 0).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.tableEvaulaltion.item(0, 1).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.tableEvaulaltion.item(0, 2).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.tableEvaulaltion.item(0, 3).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.tableEvaulaltion.item(0, 4).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.tableEvaulaltion.item(0, 5).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
