from PyQt5.QAxContainer import QAxWidget
from PyQt5.QtCore import QEventLoop

from kiwoom.win_login_connect_state import LoginConnectStateWindow
from kiwoom.win_my_info import MyInfoWindow
from kiwoom.win_deposit_info import DepositInfoWindow
from kiwoom.win_account_balance_info import AccountBalanceInfoWindow
from kiwoom.win_uncontract_info import UncontractInfoWindow
from kiwoom.win_realtime import RealtimeWindow
from kiwoom.win_condition_search import ConditionSearchWindow
from kiwoom.win_trader import TraderWindow
from kiwoom.win_order import OrderWindow

from kiwoom.worker import Worker

# referer : https://goni9071.tistory.com/263

class Kiwoom(QAxWidget):
    def __init__(self, mainWindow):
        super().__init__()

        self.mainWindow = mainWindow

        # 이벤트 루프 관련 변수
        self.login_event_loop = QEventLoop()  # 로그인 담당 이벤트 루프
        self.tr_event_loop = QEventLoop()

        # 계좌 관련 변수
        self.account_number = None
        self.total_buy_money = None
        self.total_evaluation_money = None
        self.total_evaluation_profit_and_loss_money = None
        self.total_yield = None
        self.account_stock_dict = {}
        self.not_signed_account_dict = {}

        # 예수금 관련 변수
        self.deposit = None
        self.withdraw_deposit = None
        self.order_deposit = None

        # 종목 분석 관련 변수
        self.calculator_list = []

        # 보유종목 정보
        # self.opw00018Data = {'accountEvaluation': [], 'stocks': []}
        self.opw00018Data = {'accountEvaluation': {}, 'stocks': []}
        self.opw00001Data = {}
        # 화면 번호
        """
        화면번호는 서버에 조회나 주문등 필요한 기능을 요청할때 이를 구별하기 위한 키값으로 이해하시면 됩니다. 
        0000(혹은 0)을 제외한 임의의 숫자를 사용하시면 되는데 개수가 200개로 한정되어 있기 때문에 이 개수를 넘지 않도록 관리하셔야 합니다. 
        만약 사용하는 화면번호가 200개를 넘는 경우 조회 결과나 주문 결과에 다른 데이터가 섞이거나 원하지 않는 결과가 나타날 수 있습니다.
        """
        self.screen_my_account = "1000"
        self.screen_calculation_stock = "2000"

        self.remained_data = False

        # signal 처리
        # elf.signal = pyqtSignal(str, str, str)
        self.worker = Worker()
        self.worker.signal_login.connect(self.signal_login)
        self.worker.signal_on_receive_tr_data.connect(self.signal_on_receive_tr_data)

    def signal_login(self):
        self.login_event_loop.exit()
        pass

    def signal_on_receive_tr_data(self, src_no, rq_name, tr_code, record_name, prev_next):
        if prev_next == '2':
            self.remained_data = True
        else:
            self.remained_data = False

        if rq_name == "예수금상세현황요청":
            self.onreceive_tr_data_withholdings(tr_code, rq_name)
        elif rq_name == "계좌평가잔고내역요청":
            self.onreceive_tr_data_account_evaluation_balance(tr_code, rq_name, prev_next)
        elif rq_name == "실시간미체결요청":
            self.onreceive_tr_data_realtime_pending(src_no, tr_code, rq_name, prev_next)
        elif rq_name == "주식일봉차트조회요청":
            self.onreceive_tr_data_daily_stock_chart(tr_code, rq_name, prev_next)

    def connect(self):
        """
        connect
        :return:
        """
        self.create_kiwoom_instance()
        self.event_collection()  # 이벤트와 슬롯을 메모리에 먼저 생성.
        self.login()

    def create_kiwoom_instance(self):
        """
        COM 오브젝트 생성.
        :return:
        """
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")  # 레지스트리에 저장된 키움 openAPI 모듈 불러오기

    def event_collection(self):
        self.OnReceiveMsg.connect(self.worker.on_receive_message)

        # 로그인 버전처리
        # self.OnEventConnect.connect(self.E_OnEventConnect)  # 로그인 관련 이벤트 (CommConnect)
        self.OnEventConnect.connect(self.worker.on_event_connect)  # 로그인 관련 이벤트 (CommConnect)

        # 조회와 실시간 데이터 처리
        # 일시적으로 데이터를 조회
        self.OnReceiveTrData.connect(self.worker.on_receive_tr_data)  # 트랜잭션 요청 관련 이벤트 (CommRqData)
        # 실시간으로 데이타 조회
        self.OnReceiveRealData.connect(self.worker.on_receive_real_data)  # 실시간 데이타 처리시

        # # # 조건검색식 관련
        # self.OnReceiveTrCondition.connect(self.worker.on_receive_tr_condition)
        # self.OnReceiveConditionVer.connect(self.worker.on_receive_condition_ver)

    def login(self):
        """
        로그인
        :return:
        """
        self.dynamicCall("CommConnect()")  # 시그널 함수 호출.
        self.login_event_loop.exec_()  # E_OnEventConnect

    def is_login(self):
        return self.dynamicCall("GetConnectState()")  # 시그널 함수 호출.

    def get_login_info(self, tag):
        ret = self.dynamicCall("GetLoginInfo(QString)", tag)
        return ret

    def get_code_list_by_market(self, market):
        code_list = self.dynamicCall("GetCodeListByMarket(QString)", market)
        code_list = code_list.split(';')
        return code_list[:-1]

    # def get_code_list_by_market(self, market_code):
    #     code_list = self.dynamicCall("GetCodeListByMarket(QString)", market_code)
    #     code_list = code_list.split(";")[:-1]
    #     return code_list

    def get_master_code_name(self, code):
        code_name = self.dynamicCall("GetMasterCodeName(QString)", code)
        return code_name

    def set_input_value(self, name, value):
        self.dynamicCall("SetInputValue(QString, QString)", name, value)

    def comm_rq_data(self, rq_name, tr_code, next_no, screen_no):
        """
        self.OnReceiveTrData.connect(self.worker.on_receive_tr_data)
        :param rq_name:
        :param tr_code:
        :param next_no:
        :param screen_no:
        :return:
            tr_code:
            opw00001('예수금상세현황요청'), opw00018('계좌평가잔고내역요청'),
            opt10075('실시간미체결요청'), opt10081('주식일봉차트조회요청'), opt10001('종목정보요청')
        """
        self.dynamicCall("CommRqData(QString, QString, int, QString", rq_name, tr_code, next_no, screen_no)
        self.tr_event_loop.exec_()

    def _comm_get_data(self, code, real_type, field_name, index, item_name):
        """
        CommGetData (지원하지 않을 계획) => GetCommData
        :param code:
        :param real_type:
        :param field_name:
        :param index:
        :param item_name:
        :return:
        """
        ret = self.dynamicCall("CommGetData(QString, QString, QString, int, QString", code,
                               real_type, field_name, index, item_name)
        return ret.strip()

    def get_comm_data(self, tr_code, rq_name, index, item_name):
        ret = self.dynamicCall("GetCommData(QString, QString, int, QString", tr_code,
                               rq_name, index, item_name)
        return ret.strip()

    def get_repeat_cnt(self, tr_code, rq_name):
        """
        조회수신한 멀티데이터의 갯수(반복)수를 얻을수 있습니다. 예를들어 차트조회는 한번에 최대 900개 데이터를 수신할 수 있는데
        이렇게 수신한 데이터갯수를 얻을때 사용합니다.
        이 함수는 반드시 OnReceiveTRData()이벤트 함수가 호출될때 그 안에서 사용해야 합니다.
        :param tr_code:
        :param rq_name:
        :return:
        """
        ret = self.dynamicCall("GetRepeatCnt(QString, QString)", tr_code, rq_name)
        return ret

    def cancel_screen_number(self, scr_no):
        self.dynamicCall("DisconnectRealData(QString)", scr_no)

    def send_order(self, rqname, screen_no, acc_no, order_type, code, quantity, price, hoga, order_no):
        self.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)",
                         [rqname, screen_no, acc_no, order_type, code, quantity, price, hoga, order_no])

    def get_chejan_data(self, fid):
        ret = self.dynamicCall("GetChejanData(int)", fid)
        return ret

    def send_condition(self, screen_no, condition_name, condition_index, is_realtime):
        print("[sendCondition]")
        """
        종목 조건검색 요청 메서드

        이 메서드로 얻고자 하는 것은 해당 조건에 맞는 종목코드이다.
        해당 종목에 대한 상세정보는 setRealReg() 메서드로 요청할 수 있다.
        요청이 실패하는 경우는, 해당 조건식이 없거나, 조건명과 인덱스가 맞지 않거나, 조회 횟수를 초과하는 경우 발생한다.

        조건검색에 대한 결과는
        1회성 조회의 경우, receiveTrCondition() 이벤트로 결과값이 전달되며
        실시간 조회의 경우, receiveTrCondition()과 receiveRealCondition() 이벤트로 결과값이 전달된다.

        :param screen_no: 화면번호
        :type screen_no: string
        :param condition_name: string - 조건식 이름
        :param condition_index: int - 조건식 인덱스
        :param is_realtime: int - 조건검색 조회구분(0: 1회성 조회, 1: 실시간 조회)
        """

        isRequest = self.dynamicCall("SendCondition(QString, QString, int, int",
                                     screen_no, condition_name, condition_index, is_realtime)

        if not isRequest:
            print("sendCondition(): 조건검색 요청 실패")

        # self.receiveTrCondition() # 이벤트 메서드에서 루프 종료
        # self.condition_serarch_event_loop.exec_()


    def send_condition_stop(self, screen_no, condition_name, condition_index):
        print("[sendConditionStop]")
        """ 
            종목 조건검색 중지 메서드 
        """
        self.dynamicCall("SendConditionStop(QString, QString, int)", screen_no, condition_name, condition_index)

    #
    # def get_account_number(self):
    #     account_list = self.get_login_info("ACCNO")
    #     account_number = account_list.split(';')[0]
    #     self.account_number = account_number
    #

    def get_deposit_info(self, account_number, prev_next, scr_number):
        """
        예수금상세현황요청
        :param account_number:
        :param prev_next:
        :param scr_number:
        :return:
        """
        self.account_number = account_number
        self.screen_my_account = scr_number

        self.set_input_value("계좌번호", account_number)
        self.set_input_value("비밀번호", " ")
        self.set_input_value("비밀번호입력매체구분", "00")
        self.set_input_value("조회구분", "2")
        self.comm_rq_data("예수금상세현황요청", "opw00001", prev_next, scr_number)

        # self.account_event_loop.exec_()

    def get_account_evaluation_balance(self, account_number, prev_next, scr_number):
        """
        계좌평가잔고내역요청
        :param account_number:
        :param prev_next:
        :param scr_number:
        :return:
        """
        print('get_account_evaluation_balance', account_number, prev_next, scr_number)
        self.account_number = account_number
        self.screen_my_account = scr_number

        self.set_input_value("계좌번호", account_number)
        self.set_input_value("비밀번호", " ")
        self.set_input_value("비밀번호입력매체구분", "00")
        self.set_input_value("조회구분", "1")
        self.comm_rq_data("계좌평가잔고내역요청", "opw00018", prev_next, scr_number)

        # if not self.account_event_loop.isRunning():
        #     print('account_event_loop.exec_() start')
        #     self.account_event_loop.exec_()

    def not_signed_account(self, nPrevNext=0):
        self.set_input_value("계좌번호", self.account_number)
        self.set_input_value("전체종목구분", "0")
        self.set_input_value("매매구분", "0")
        self.set_input_value("체결구분", "1")
        self.comm_rq_data("실시간미체결요청", "opt10075", nPrevNext, self.screen_my_account)
        #
        # if not self.account_event_loop.isRunning():
        #     self.account_event_loop.exec_()

    # 각각의 윈도우 열기 시작
    def login_connect_state(self):
        """
        로그인 상태 관련
        :return:
        """
        self.winLoginConnectState = LoginConnectStateWindow(self)
        self.winLoginConnectState.show()
        # os.system('cls')
        # input()

    def my_info(self):
        """
        사용자정보 조회
        :return:
        """
        self.winMyInfoWindow = MyInfoWindow(self)
        self.winMyInfoWindow.show()

    def deposit_info(self):
        """
        예수금 조회
        :return:
        """
        self.winDepositInfoWindow = DepositInfoWindow(self)
        self.winDepositInfoWindow.show()

    def account_evaulation_balance_info(self):
        """
        평가금액 정보
        :return:
        """
        self.winAccountBalanceInfoWindow = AccountBalanceInfoWindow(self)
        self.winAccountBalanceInfoWindow.show()

    def uncontract_info(self):
        """
        미체결 내역 정보
        :return:
        """
        self.winUncontractInfoWindow = UncontractInfoWindow(self)
        self.winUncontractInfoWindow.show()

    def realtime(self):
        """
        실시간 거래데이타 가져오기
        :return:
        """
        self.realtimeWindow = RealtimeWindow(self)
        self.realtimeWindow.show()

    def conditionSearch(self):
        """
        조건검색
        :return:
        """
        self.conditionSearchWindow = ConditionSearchWindow(self)
        self.conditionSearchWindow.show()

    def trader(self):
        """
        조건식을 이용한 tracer 창
        :return:
        """
        self.traderhWindow = TraderWindow(self)
        self.traderhWindow.show()

    def order(self):
        """
        order 윈도우
        :return:
        """
        self.orderWindow = OrderWindow(self)
        self.orderWindow.show()
        pass

    ## 각각의 윈도우 열기 끝


    ### Event 함수 ###
    ## 공통 ##

    ## 조회와 실시간 데이터 처리 ##

    def onreceive_tr_data_withholdings(self, tr_code, rq_name):
        """
        예수금상세현황요청 (opw00001)
        :param tr_code:
        :param rq_name:
        :return:
        """
        keyList = ['예수금', '출금가능금액', '주문가능금액', 'd+2추정예수금']
        for key in keyList:
            value = self.get_comm_data(tr_code, rq_name, 0, key)
            value = self.change_format(value)
            self.opw00001Data[key] = value

        print('opw00001Data', self.opw00001Data)
        self.cancel_screen_number(self.screen_my_account)
        self.tr_event_loop.exit()

    def onreceive_tr_data_account_evaluation_balance(self, tr_code, rq_name, prev_next):
        """
        계좌평가잔고내역요청 (opw00018)
        :param tr_code:
        :param rq_name:
        :param prev_next:
        :return:
        """

        print('onreceive_tr_data_account_evaluation_balance start');
        # if (self.total_buy_money == None or self.total_evaluation_money == None
        #         or self.total_evaluation_profit_and_loss_money == None or self.total_yield == None):
        accountEvaluation = {}
        keyList = ['총매입금액', '총평가금액', '총평가손익금액', '총수익률(%)', '추정예탁자산']

        for key in keyList:
            value = self.get_comm_data(tr_code, rq_name, 0, key)

            if key.startswith("총수익률"):
                value = self.change_format(value, 1)
            else:
                value = self.change_format(value)

            # accountEvaluation.append(value)
            accountEvaluation[key] = value

        self.opw00018Data['accountEvaluation'] = accountEvaluation

        print('opw00018Data', self.opw00018Data)

        cnt = self.get_repeat_cnt(tr_code, rq_name)
        for i in range(cnt):
            stock_code = self.get_comm_data(tr_code, rq_name, i, '종목번호')
            stock_code = stock_code.strip()[1:]

            stock_name = self.get_comm_data(tr_code, rq_name, i, '종목명')
            stock_name = stock_name.strip()  # 필요 없는 공백 제거.

            stock_evaluation_profit_and_loss = self.get_comm_data(tr_code, rq_name, i, '평가손익')
            # stock_evaluation_profit_and_loss = int(stock_evaluation_profit_and_loss)
            stock_evaluation_profit_and_loss = self.change_format(stock_evaluation_profit_and_loss)


            stock_yield = self.get_comm_data(tr_code, rq_name, i, '수익률(%)')
            stock_yield = float(stock_yield)

            stock_buy_money = self.get_comm_data(tr_code, rq_name, i, '매입가')
            stock_buy_money = self.change_format(stock_buy_money)
            # stock_buy_money = int(stock_buy_money)

            stock_quantity = self.get_comm_data(tr_code, rq_name, i, '보유수량')
            stock_quantity = self.change_format(stock_quantity)
            # stock_quantity = int(stock_quantity)

            stock_trade_quantity = self.get_comm_data(tr_code, rq_name, i, '매매가능수량')
            stock_trade_quantity = self.change_format(stock_trade_quantity)
            # stock_trade_quantity = int(stock_trade_quantity)

            stock_present_price = self.get_comm_data(tr_code, rq_name, i, '현재가')
            stock_present_price = self.change_format(stock_present_price)
            # stock_present_price = int(stock_present_price)

            if not stock_code in self.account_stock_dict:
                self.account_stock_dict[stock_code] = {}

            self.account_stock_dict[stock_code].update({'종목명': stock_name})
            self.account_stock_dict[stock_code].update(
                {'평가손익': stock_evaluation_profit_and_loss})
            self.account_stock_dict[stock_code].update(
                {'수익률(%)': stock_yield})
            self.account_stock_dict[stock_code].update(
                {'매입가': stock_buy_money})
            self.account_stock_dict[stock_code].update(
                {'보유수량': stock_quantity})
            self.account_stock_dict[stock_code].update(
                {'매매가능수량': stock_trade_quantity})
            self.account_stock_dict[stock_code].update(
                {'현재가': stock_present_price})

        if prev_next == "2":
            self.get_account_evaluation_balance(self.account_number, 2, self.screen_my_account)
        else:
            self.cancel_screen_number(self.screen_my_account)
            self.tr_event_loop.exit()

    def onreceive_tr_data_realtime_pending(self, scr_no, tr_code, rq_name, prev_next):
        """
        실시간미체결요청 (opt10075)
        :param scr_no:
        :param tr_code:
        :param rq_name:
        :param prev_next:
        :return:
        """
        cnt = self.get_repeat_cnt(tr_code, rq_name)

        for i in range(cnt):
            stock_code = self.get_comm_data(tr_code, rq_name, i, '종목코드')
            stock_code = stock_code.strip()

            stock_order_number = self.get_comm_data(tr_code, rq_name, i, '주문번호')
            stock_order_number = int(stock_order_number)

            stock_name = self.get_comm_data(tr_code, rq_name, i, '종목명')
            stock_name = stock_name.strip()

            stock_order_type = self.get_comm_data(tr_code, rq_name, i, '주문구분')
            stock_order_type = stock_order_type.strip().lstrip('+').lstrip('-')

            stock_order_price = self.get_comm_data(tr_code, rq_name, i, '주문가격')
            stock_order_price = int(stock_order_price)

            stock_order_quantity = self.get_comm_data(tr_code, rq_name, i, '주문수량')
            stock_order_quantity = int(stock_order_quantity)

            stock_not_signed_quantity = self.get_comm_data(tr_code, rq_name, i, '미체결수량')
            stock_not_signed_quantity = int(stock_not_signed_quantity)

            stock_signed_quantity = self.get_comm_data(tr_code, rq_name, i, '체결량')
            stock_signed_quantity = int(stock_signed_quantity)

            stock_present_price = self.get_comm_data(tr_code, rq_name, i, '현재가')
            stock_present_price = int(
                stock_present_price.strip().lstrip('+').lstrip('-'))

            stock_order_status = self.get_comm_data(tr_code, rq_name, i, '주문상태')
            stock_order_status = stock_order_status.strip()

            if not stock_order_number in self.not_signed_account_dict:
                self.not_signed_account_dict[stock_order_number] = {}

            self.not_signed_account_dict[stock_order_number].update(
                {'종목코드': stock_code})
            self.not_signed_account_dict[stock_order_number].update(
                {'종목명': stock_name})
            self.not_signed_account_dict[stock_order_number].update(
                {'주문구분': stock_order_type})
            self.not_signed_account_dict[stock_order_number].update(
                {'주문가격': stock_order_price})
            self.not_signed_account_dict[stock_order_number].update(
                {'주문수량': stock_order_quantity})
            self.not_signed_account_dict[stock_order_number].update(
                {'미체결수량': stock_not_signed_quantity})
            self.not_signed_account_dict[stock_order_number].update(
                {'체결량': stock_signed_quantity})
            self.not_signed_account_dict[stock_order_number].update(
                {'현재가': stock_present_price})
            self.not_signed_account_dict[stock_order_number].update(
                {'주문상태': stock_order_status})

        if prev_next == "2":
            self.not_signed_account(2)
        else:
            self.cancel_screen_number(scr_no)
            self.tr_event_loop.exit()

    def onreceive_tr_data_daily_stock_chart(self, tr_code, rq_name, prev_next):
        """
        주식일봉차트조회요청 (opt10081)
        :param tr_code:
        :param rq_name:
        :param prev_next:
        :return:
        """
        stock_code = self.get_comm_data(tr_code, rq_name, 0, '종목코드')
        # six_hundred_data = self.dynamicCall("GetCommDataEx(QString, QString)", sTrCode, sRQName)

        stock_code = stock_code.strip()
        cnt = self.get_repeat_cnt(tr_code, rq_name)  # 최대 600일

        for i in range(cnt):
            calculator_list = []

            current_price = self.get_comm_data(tr_code, rq_name, i, '현재가')
            volume = self.get_comm_data(tr_code, rq_name, i, '거래량')
            trade_price = self.get_comm_data(tr_code, rq_name, i, '거래대금')
            date = self.get_comm_data(tr_code, rq_name, i, '일자')
            start_price = self.get_comm_data(tr_code, rq_name, i, '시가')
            high_price = self.get_comm_data(tr_code, rq_name, i, '고가')
            low_price = self.get_comm_data(tr_code, rq_name, i, '저가')

            calculator_list.append("")
            calculator_list.append(int(current_price))
            calculator_list.append(int(volume))
            calculator_list.append(int(trade_price))
            calculator_list.append(int(date))
            calculator_list.append(int(start_price))
            calculator_list.append(int(high_price))
            calculator_list.append(int(low_price))
            calculator_list.append("")

            self.calculator_list.append(calculator_list.copy())

        if prev_next == "2":
            self.day_kiwoom_db(stock_code, None, 2)
        else:
            self.tr_event_loop.exit()

    # def E_OnReceiveTrData(self, sScrNo, sRQName, sTrCode, sRecordName, sPrevNext):
    #     if sPrevNext == '2':
    #         self.remained_data = True
    #     else:
    #         self.remained_data = False
    #
    #     if sRQName == "예수금상세현황요청":
    #         self.onreceive_tr_data_withholdings(sTrCode, sRQName)
    #     elif sRQName == "계좌평가잔고내역요청":
    #         self.onreceive_tr_data_account_evaluation_balance(sTrCode, sRQName, sPrevNext)
    #     elif sRQName == "실시간미체결요청":
    #         self.onreceive_tr_data_realtime_pending(sScrNo, sTrCode, sRQName, sPrevNext)
    #     elif sRQName == "주식일봉차트조회요청":
    #         self.onreceive_tr_data_daily_stock_chart(sTrCode, sRQName, sPrevNext)

    # def E_OnReceiveRealData(self, sCode, sRealType, sRealData):
    #     """
    #     :param sRealType: 주식예상체결, 장시작시간, 주식우선호가, 주식당일거래원
    #     :param sRealData :
    #         주식우선호가: +79900	+79800
    #         주식예상체결: sRealData 152707	+79900	+200	+0.25	--212	715156	2
    #         주식체결: 153028	+79800	+100	+0.13	+79900	+79800	 774560	9700742	775794	+80000	+80200	+79800
    #         2	-67366	-3348496884	-99.31	0.16	208	70.86	4763886	2	0	-99.57	000000	000000	10022	090008
    #         094034	153028	5101149	3614467	-41.47	46716	28239	 61809888	 0	 0	 0	7980	6384	79973	425
    #         주식당일거래원: JP모간서울	1184351	+314738	033	DHDB	한  화	1038978	+24113	021	!!!!	이베스트	944407	+514	063	!!!! .....
    #         장시작시간 : 8	888888	000000
    #         장시작시간 : 2	152700	000300
    #     :param sCode:
    #     :param sRealType:
    #     :param sRealData:
    #     :return:
    #     """
    #     print('sCode', sCode)
    #     print('sRealType', sRealType)
    #     print('sRealData', sRealData)
    #
    #     if sRealType == '주식체결':
    #         user_signal = pyqtSignal()
    #         if self.realtimeWindow:
    #             user_signal.emit(self.realtimeWindow.user_slot)
    #         pass


    # def calculator(self):
    #     print('calculator start')
    #     kosdaq_list = self.get_code_list_by_market("10")
    #
    #     self.day_kiwoom_db(900300)
    #
    #     # for idx, stock_code in enumerate(kosdaq_list):
    #     #     self.dynamicCall("DisconnectRealData(QString)",
    #     #                      self.screen_calculation_stock)
    #     #
    #     #     print(
    #     #         f"{idx + 1} / {len(kosdaq_list)} : KOSDAQ Stock Code : {stock_code} is updating...")
    #     #     self.day_kiwoom_db(stock_code)

    def day_kiwoom_db(self, stock_code=None, date=None, nPrevNext=0):
        print('day_kiwoom_db start')
        # QTest.qWait(100)  # 0.1초마다 딜레이
        # QTest.qWait(3600)  # 3.6초마다 딜레이
        # self.set_input_value("종목코드", stock_code)
        # self.set_input_value("수정주가구분", 1)
        #
        # if date != None:  # date가 None일 경우 date는 오늘 날짜 기준
        #     self.set_input_value("기준일자", date)
        #
        # self.comm_rq_data("주식일봉차트조회요청", "opt10081", nPrevNext, self.screen_calculation_stock)
        #
        # if not self.tr_event_loop.isRunning():
        #     self.tr_event_loop.exec_()


    def getConditionNameList(self):
        print("[getConditionNameList]")
        """
        조건식 획득 메서드

        조건식을 딕셔너리 형태로 반환합니다.
        이 메서드는 반드시 receiveConditionVer() 이벤트 메서드안에서 사용해야 합니다.

        :return: dict - {인덱스:조건명, 인덱스:조건명, ...}
        """

        data = self.dynamicCall("GetConditionNameList()")

        if data == "":
            print("getConditionNameList(): 사용자 조건식이 없습니다.")


        conditionList = data.split(';')
        del conditionList[-1]

        conditionDictionary = {}

        for condition in conditionList:
            key, value = condition.split('^')
            conditionDictionary[int(key)] = value

        return conditionDictionary

    def change_format(self, data, percent=0):
        formatData = ''
        if data:
            if percent == 0:
                d = int(data)
                formatData = '{:-,d}'.format(d)

            elif percent == 1:
                f = int(data) / 100
                formatData = '{:-,.2f}'.format(f)

            elif percent == 2:
                f = float(data)
                formatData = '{:-,.2f}'.format(f)

        return formatData