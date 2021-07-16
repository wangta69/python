from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5 import uic
from PyQt5.QtCore import QEventLoop

import time
from kiwoom.worker import Worker

form_class = uic.loadUiType("ui/kiwoom/main.ui")[0]

## referer : https://wikidocs.net/

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
            pass

        self.set_account_combo()

        self.pushButtonSetOrder.clicked.connect(self.send_order)
        self.buttonCheckBalance.clicked.connect(self.check_balance)

        # 이벤트 루프 관련 변수
        self.tr_event_loop = QEventLoop()

        self.worker = Worker()
        self.worker.signal_on_receive_tr_data.connect(self.signal_tr_data)
        self.kiwoom.OnReceiveTrData.connect(self.signal_tr_data)


    def signal_tr_data(self, src_no, rq_name, tr_code, record_name, prev_next):
        pass
        #
        # print('signal_tr_data', self, src_no, rq_name, tr_code, record_name, prev_next)
        # if prev_next == '2':
        #     self.remained_data = True
        # else:
        #     self.remained_data = False
        #
        # if prev_next == "2":
        #     self.kiwoom.set_input_value("계좌번호", self.kiwoom.account_number)
        #     self.kiwoom.comm_rq_data("계좌평가잔고내역요청", "opw00018", 0, "2000")
        # else:
        #     self.tr_event_loop.exit()


        # if rq_name == "예수금상세현황요청":
        #     self.onreceive_tr_data_withholdings(tr_code, rq_name)
        # elif rq_name == "계좌평가잔고내역요청":
        #     self.onreceive_tr_data_account_evaluation_balance(tr_code, rq_name, prev_next)
        # elif rq_name == "실시간미체결요청":
        #     self.onreceive_tr_data_realtime_pending(src_no, tr_code, rq_name, prev_next)
        # elif rq_name == "주식일봉차트조회요청":
        #     self.onreceive_tr_data_daily_stock_chart(tr_code, rq_name, prev_next)

    def set_account_combo(self):
        accouns_num = int(self.kiwoom.get_login_info("ACCOUNT_CNT"))
        accounts = self.kiwoom.get_login_info("ACCNO")
        accounts_list = accounts.split(';')[0:accouns_num]
        self.comboAccount.addItems(accounts_list)


    # def _set_signal_slots(self):
    #     self.OnEventConnect.connect(self._event_connect)
    #     self.OnReceiveTrData.connect(self._receive_tr_data)

    # def comm_connect(self):
    #     self.dynamicCall("CommConnect()")
    #     self.login_event_loop = QEventLoop()
    #     self.login_event_loop.exec_()

    # def _event_connect(self, err_code):
    #     if err_code == 0:
    #         print("connected")
    #     else:
    #         print("disconnected")
    #
    #     self.login_event_loop.exit()

    def get_code_list_by_market(self, market):
        code_list = self.kiwoom.dynamicCall("GetCodeListByMarket(QString)", market)
        code_list = code_list.split(';')
        return code_list[:-1]

    def get_master_code_name(self, code):
        code_name = self.kiwoom.dynamicCall("GetMasterCodeName(QString)", code)
        return code_name

    def get_connect_state(self):
        ret = self.kiwoom.dynamicCall("GetConnectState()")
        return ret

    def set_input_value(self, id, value):
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", id, value)

    def comm_rq_data(self, rqname, trcode, next, screen_no):
        self.kiwoom.dynamicCall("CommRqData(QString, QString, int, QString)", rqname, trcode, next, screen_no)
        self.tr_event_loop = QEventLoop()
        self.tr_event_loop.exec_()

    def _comm_get_data(self, code, real_type, field_name, index, item_name):
        ret = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", code,
                               real_type, field_name, index, item_name)
        return ret.strip()

    def _get_repeat_cnt(self, trcode, rqname):
        ret = self.kiwoom.dynamicCall("GetRepeatCnt(QString, QString)", trcode, rqname)
        return ret

    # def _receive_tr_data(self, screen_no, rqname, trcode, record_name, next, unused1, unused2, unused3, unused4):
    #     if next == '2':
    #         self.remained_data = True
    #     else:
    #         self.remained_data = False
    #
    #     if rqname == "계좌평가잔고내역요청":
    #         self._opt10081(rqname, trcode)
    #
    #     try:
    #         self.tr_event_loop.exit()
    #     except AttributeError:
    #         pass

    def _opt10081(self, rqname, trcode):
        data_cnt = self._get_repeat_cnt(trcode, rqname)

        for i in range(data_cnt):
            date = self._comm_get_data(trcode, "", rqname, i, "일자")
            open = self._comm_get_data(trcode, "", rqname, i, "시가")
            high = self._comm_get_data(trcode, "", rqname, i, "고가")
            low = self._comm_get_data(trcode, "", rqname, i, "저가")
            close = self._comm_get_data(trcode, "", rqname, i, "현재가")
            volume = self._comm_get_data(trcode, "", rqname, i, "거래량")

            self.ohlcv['date'].append(date)
            self.ohlcv['open'].append(int(open))
            self.ohlcv['high'].append(int(high))
            self.ohlcv['low'].append(int(low))
            self.ohlcv['close'].append(int(close))
            self.ohlcv['volume'].append(int(volume))

    # def send_order(self):
    #     order_type_lookup = {'신규매수': 1, '신규매도': 2, '매수취소': 3, '매도취소': 4}
    #     hoga_lookup = {'지정가': "00", '시장가': "03"}
    #
    #     account = self.comboAccount.currentText()
    #     order_type = self.comboOrderType.currentText()
    #     code = self.lineEdit.text()
    #     hoga = self.comboBox_3.currentText()
    #     num = self.spinQuantity.value()
    #     price = self.spinBoxPrice.value()
    #
    #     self.kiwoom.send_order("send_order_req", "0101", account, order_type_lookup[order_type], code, num, price,
    #                            hoga_lookup[hoga], "")

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

    def get_chejan_data(self, fid):
        ret = self.kiwoom.get_chejan_data(fid)
        return ret

    def code_changed(self):
        code = self.lineEdit.text()
        name = self.kiwoom.get_master_code_name(code)
        self.lineEdit_2.setText(name)

    def reset_opw00018_output(self):
        self.opw00018_output = {'single': [], 'multi': []}

    def check_balance(self):
        self.reset_opw00018_output()
        self.kiwoom.account_number = self.comboAccount.currentText()
        self.kiwoom.get_account_evaluation_balance(self.kiwoom.account_number, 0, "2000")

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