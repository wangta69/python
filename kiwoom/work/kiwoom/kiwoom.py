from PyQt5.QAxContainer import QAxWidget
from PyQt5.QtCore import QEventLoop
# from kiwoom.config.errCode import *
from kiwoom.win_login_connect_state import LoginConnectStateWindow
from kiwoom.win_my_info import MyInfoWindow
from kiwoom.win_deposit_info import DepositInfoWindow
from kiwoom.win_account_balance_info import AccountBalanceInfoWindow
from kiwoom.win_uncontract_info import UncontractInfoWindow
from kiwoom.win_realtime import RealtimeWindow
from kiwoom.win_condition_search import ConditionSearchWindow
from kiwoom.win_order import OrderWindow
class Kiwoom(QAxWidget):
    def __init__(self, mainWindow):
        super().__init__()

        self.mainWindow = mainWindow

        # 이벤트 루프 관련 변수
        self.login_event_loop = QEventLoop()  # 로그인 담당 이벤트 루프
        self.account_event_loop = QEventLoop()
        self.calculator_event_loop = QEventLoop()
        self.tr_event_loop = QEventLoop()


        # # 초기 작업
        # self.create_kiwoom_instance()
        # self.event_collection()  # 이벤트와 슬롯을 메모리에 먼저 생성.
        # # self.login()

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

        # 화면 번호
        """
        화면번호는 서버에 조회나 주문등 필요한 기능을 요청할때 이를 구별하기 위한 키값으로 이해하시면 됩니다. 
        0000(혹은 0)을 제외한 임의의 숫자를 사용하시면 되는데 개수가 200개로 한정되어 있기 때문에 이 개수를 넘지 않도록 관리하셔야 합니다. 
        만약 사용하는 화면번호가 200개를 넘는 경우 조회 결과나 주문 결과에 다른 데이터가 섞이거나 원하지 않는 결과가 나타날 수 있습니다.
        """
        self.screen_my_account = "1000"
        self.screen_calculation_stock = "2000"

        self.remained_data = False

        # 초기 작업
        # self.create_kiwoom_instance()
        # self.event_collection()  # 이벤트와 슬롯을 메모리에 먼저 생성.
        # # self.login()
        # self.get_account_number()  # 계좌 번호만 얻어오기
        # self.get_deposit_info()  # 예수금 관련된 정보 얻어오기
        # self.get_account_evaluation_balance()  # 계좌평가잔고내역 얻어오기
        # self.not_signed_account()  # 미체결내역 얻어오기
        # self.calculator()
      #  self.menu()

    # -------------------------------------
    # connect
    # -------------------------------------
    def connect(self):
        self.create_kiwoom_instance()
        self.event_collection()  # 이벤트와 슬롯을 메모리에 먼저 생성.
        self.login()
        # self.get_account_number()  # 계좌 번호만 얻어오기
        # self.get_deposit_info()  # 예수금 관련된 정보 얻어오기
        # self.get_account_evaluation_balance()  # 계좌평가잔고내역 얻어오기
        # self.not_signed_account()  # 미체결내역 얻어오기
        # self.calculator()

    # COM 오브젝트 생성.
    def create_kiwoom_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")  # 레지스트리에 저장된 키움 openAPI 모듈 불러오기

    def event_collection(self):
        self.OnReceiveMsg.connect(self.E_OnReceiveMsg)

        # 로그인 버전처리
        self.OnEventConnect.connect(self.E_OnEventConnect)  # 로그인 관련 이벤트

        # 조회와 실시간 데이터 처리
        self.OnReceiveTrData.connect(self.E_OnReceiveTrData)   # 트랜잭션 요청 관련 이벤트
        self.OnReceiveRealData.connect(self.E_OnReceiveRealData)
        
        # # 조건검색식 관련
        # self.OnReceiveConditionVer.connect(self.E_OnReceiveConditionVer)
    # -------------------------------------
    # 로그인 관련
    # -------------------------------------
    def login(self):
        self.dynamicCall("CommConnect()")  # 시그널 함수 호출.
        self.login_event_loop.exec_() # E_OnEventConnect

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

    def comm_rq_data(self, rqname, trcode, next, screen_no):
        self.dynamicCall("CommRqData(QString, QString, int, QString", rqname, trcode, next, screen_no)
        self.tr_event_loop.exec_()

    ## CommGetData (지원하지 않을 계획) => GetCommData
    def _comm_get_data(self, code, real_type, field_name, index, item_name):
        ret = self.dynamicCall("CommGetData(QString, QString, QString, int, QString", code,
                               real_type, field_name, index, item_name)
        return ret.strip()

    def get_comm_data(self, tr_code, rq_name, index, item_name):
        ret = self.dynamicCall("GetCommData(QString, QString, int, QString", tr_code,
                               rq_name, index, item_name)
        return ret.strip()

    def get_repeat_cnt(self, tr_code, rq_name):
        ret = self.dynamicCall("GetRepeatCnt(QString, QString)", tr_code, rq_name)
        return ret

    def cancel_screen_number(self, scr_no):
        self.dynamicCall("DisconnectRealData(QString)", scr_no)


    #
    # def get_account_number(self):
    #     account_list = self.get_login_info("ACCNO")
    #     account_number = account_list.split(';')[0]
    #     self.account_number = account_number
    #
    # def get_deposit_info(self, nPrevNext=0):
    #     self.set_input_value("계좌번호", self.account_number)
    #     self.set_input_value("비밀번호", " ")
    #     self.set_input_value("비밀번호입력매체구분", "00")
    #     self.set_input_value("조회구분", "2")
    #     self.comm_rq_data("예수금상세현황요청", "opw00001", nPrevNext, self.screen_my_account)
    #
    #     self.account_event_loop.exec_()
    #
    def get_account_evaluation_balance(self, nPrevNext=0):
        self.set_input_value("계좌번호", self.account_number)
        self.set_input_value("비밀번호", " ")
        self.set_input_value("비밀번호입력매체구분", "00")
        self.set_input_value("조회구분", "1")
        self.comm_rq_data("계좌평가잔고내역요청", "opw00018", nPrevNext, self.screen_my_account)

        if not self.account_event_loop.isRunning():
            self.account_event_loop.exec_()

    def not_signed_account(self, nPrevNext=0):
        self.set_input_value("계좌번호", self.account_number)
        self.set_input_value("전체종목구분", "0")
        self.set_input_value("매매구분", "0")
        self.set_input_value("체결구분", "1")
        self.comm_rq_data("실시간미체결요청", "opt10075", nPrevNext, self.screen_my_account)

        if not self.account_event_loop.isRunning():
            self.account_event_loop.exec_()




    ## 각각의 윈도우 열기 시작
    # -------------------------------------
    # 로그인 상태 관련
    # -------------------------------------
    def login_connect_state(self):
        self.winLoginConnectState = LoginConnectStateWindow(self)
        self.winLoginConnectState.show()
        # os.system('cls')
        # input()

    # -------------------------------------
    # 사용자정보 조회
    # -------------------------------------
    def my_info(self):
        self.winMyInfoWindow = MyInfoWindow(self)
        self.winMyInfoWindow.show()

    # -------------------------------------
    # 예수금 조회
    # -------------------------------------
    def deposit_info(self):
        self.winDepositInfoWindow = DepositInfoWindow(self)
        self.winDepositInfoWindow.show()

    # -------------------------------------
    # 평가금액 정보
    # -------------------------------------
    def account_evaulation_balance_info(self):
        self.winAccountBalanceInfoWindow = AccountBalanceInfoWindow(self)
        self.winAccountBalanceInfoWindow.show()
        
    # -------------------------------------
    # 미체결 내역 정보
    # -------------------------------------
    def uncontract_info(self):
        self.winUncontractInfoWindow = UncontractInfoWindow(self)
        self.winUncontractInfoWindow.show()
        
    # -------------------------------------
    # 실시간 거래데이타 가져오기
    # -------------------------------------
    def realtime(self):
        self.realtimeWindow = RealtimeWindow(self)
        self.realtimeWindow.show()
    
    """
        조건검색
    """
    def conditionSearch(self):
        self.conditionSearchWindow = ConditionSearchWindow(self)
        self.conditionSearchWindow.show()
        pass

    """
       order 윈도우
    """
    def order(self):
        self.orderWindow = OrderWindow(self)
        self.orderWindow.show()
        pass

    ## 각각의 윈도우 열기 끝


    ### Event 함수 ###
    ## 공통 ##
    def E_OnReceiveMsg(self, sScrNo, sRQName, sTrCode, sMsg):
        print(sScrNo, sRQName, sTrCode, sMsg)
        pass

    ## 로그인 버전처리 ##
    def E_OnEventConnect(self, err_code):
        if err_code == 0:
            print("로그인 성공")
            # self.mainWindow.statusBar.showMessage("Connected")
        else:
            print("로그인 실패")
            # os.system('cls') # console을 지울때 사용 'clear for linux and mac
            # self.mainWindow.statusBar.showMessage("로그인 실패 - 에러 내용 :", errors(err_code)[1])
            # sys.exit(0)
            # print("로그인 실패 - 에러 내용 :", errors(err_code)[1])
        self.login_event_loop.exit()

    ## 조회와 실시간 데이터 처리 ##

    """
    예수금상세현황요청
    """
    def onreceive_tr_data_withholdings(self, tr_code, rq_name):
        deposit = self.get_comm_data(tr_code, rq_name, 0, '예수금')
        self.deposit = int(deposit)

        withdraw_deposit = self.get_comm_data(tr_code, rq_name, 0, '출금가능금액')
        self.withdraw_deposit = int(withdraw_deposit)

        order_deposit = self.get_comm_data(tr_code, rq_name, 0, '주문가능금액')
        self.order_deposit = int(order_deposit)

        self.cancel_screen_number(self.screen_my_account)
        self.account_event_loop.exit()

    """
    계좌평가잔고내역요청
    """
    def onreceive_tr_data_account_evaluation_balance(self, tr_code, rq_name, prev_next):
        if (self.total_buy_money == None or self.total_evaluation_money == None
                or self.total_evaluation_profit_and_loss_money == None or self.total_yield == None):
            total_buy_money = self.get_comm_data(tr_code, rq_name, 0, '총매입금액')
            self.total_buy_money = int(total_buy_money)

            total_evaluation_money = self.get_comm_data(tr_code, rq_name, 0, '총평가금액')
            self.total_evaluation_money = int(total_evaluation_money)

            total_evaluation_profit_and_loss_money = self.get_comm_data(tr_code, rq_name, 0, '총평가손익금액')
            self.total_evaluation_profit_and_loss_money = int(
                total_evaluation_profit_and_loss_money)

            total_yield = self.get_comm_data(tr_code, rq_name, 0, '총수익률(%)')
            self.total_yield = float(total_yield)

        cnt = self.get_repeat_cnt(tr_code, rq_name)

        for i in range(cnt):
            stock_code = self.get_comm_data(tr_code, rq_name, i, '종목번호')
            stock_code = stock_code.strip()[1:]

            stock_name = self.get_comm_data(tr_code, rq_name, i, '종목명')
            stock_name = stock_name.strip()  # 필요 없는 공백 제거.

            stock_evaluation_profit_and_loss = self.get_comm_data(tr_code, rq_name, i, '평가손익')
            stock_evaluation_profit_and_loss = int(
                stock_evaluation_profit_and_loss)

            stock_yield = self.get_comm_data(tr_code, rq_name, i, '수익률(%)')
            stock_yield = float(stock_yield)

            stock_buy_money = self.get_comm_data(tr_code, rq_name, i, '매입가')
            stock_buy_money = int(stock_buy_money)

            stock_quantity = self.get_comm_data(tr_code, rq_name, i, '보유수량')
            stock_quantity = int(stock_quantity)

            stock_trade_quantity = self.get_comm_data(tr_code, rq_name, i, '매매가능수량')
            stock_trade_quantity = int(stock_trade_quantity)

            stock_present_price = self.get_comm_data(tr_code, rq_name, i, '현재가')
            stock_present_price = int(stock_present_price)

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
            self.get_account_evaluation_balance(2)
        else:
            self.cancel_screen_number(self.screen_my_account)
            self.account_event_loop.exit()

    """
    실시간미체결요청
    """
    def onreceive_tr_data_realtime_pending(self, scr_no, tr_code, rq_name, prev_next):
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
            self.account_event_loop.exit()

    """
    주식일봉차트조회요청
    """
    def onreceive_tr_data_daily_stock_chart(self, tr_code, rq_name, prev_next):
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
            self.calculator_event_loop.exit()

    def E_OnReceiveTrData(self, sScrNo, sRQName, sTrCode, sRecordName, sPrevNext):
        if sPrevNext == '2':
            self.remained_data = True
        else:
            self.remained_data = False

        if sRQName == "예수금상세현황요청":
            self.onreceive_tr_data_withholdings(sTrCode, sRQName)
        elif sRQName == "계좌평가잔고내역요청":
            self.onreceive_tr_data_account_evaluation_balance(sTrCode, sRQName, sPrevNext)
        elif sRQName == "실시간미체결요청":
            self.onreceive_tr_data_realtime_pending(sScrNo, sTrCode, sRQName, sPrevNext)
        elif sRQName == "주식일봉차트조회요청":
            self.onreceive_tr_data_daily_stock_chart(sTrCode, sRQName, sPrevNext)

    """
        :param sRealType: 주식예상체결, 장시작시간, 주식우선호가, 주식당일거래원
        :param sRealData : 
            주식우선호가: +79900	+79800
            주식예상체결: sRealData 152707	+79900	+200	+0.25	--212	715156	2
            주식체결: 153028	+79800	+100	+0.13	+79900	+79800	 774560	9700742	775794	+80000	+80200	+79800	2	-67366	-3348496884	-99.31	0.16	208	70.86	4763886	2	0	-99.57	000000	000000	10022	090008	094034	153028	5101149	3614467	-41.47	46716	28239	 61809888	 0	 0	 0	7980	6384	79973	425
            주식당일거래원: JP모간서울	1184351	+314738	033	DHDB	한  화	1038978	+24113	021	!!!!	이베스트	944407	+514	063	!!!! .....
            장시작시간 : 8	888888	000000
            장시작시간 : 2	152700	000300
    """
    def E_OnReceiveRealData(self, sCode, sRealType, sRealData):
        print('sCode', sCode)
        print('sRealType', sRealType)
        print('sRealData', sRealData)


    def calculator(self):
        print('calculator start')
        kosdaq_list = self.get_code_list_by_market("10")

        self.day_kiwoom_db(900300)

        # for idx, stock_code in enumerate(kosdaq_list):
        #     self.dynamicCall("DisconnectRealData(QString)",
        #                      self.screen_calculation_stock)
        #
        #     print(
        #         f"{idx + 1} / {len(kosdaq_list)} : KOSDAQ Stock Code : {stock_code} is updating...")
        #     self.day_kiwoom_db(stock_code)

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
        # if not self.calculator_event_loop.isRunning():
        #     self.calculator_event_loop.exec_()