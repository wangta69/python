import os
from PyQt5.QAxContainer import QAxWidget
from PyQt5.QtCore import QEventLoop
# from kiwoom.config.errCode import *
from .win_login_connect_state import LoginConnectStateWindow
from .win_my_info import MyInfoWindow
from .win_deposit_info import DepositInfoWindow
from .win_account_balance_info import AccountBalanceInfoWindow
from .win_uncontract_info import UncontractInfoWindow
from .win_realtime import RealtimeWindow
from .win_condition_search import ConditionSearchWindo

class Kiwoom(QAxWidget):
    def __init__(self, mainWindow):
        super().__init__()

        self.mainWindow = mainWindow

        # 이벤트 루프 관련 변수
        self.login_event_loop = QEventLoop()  # 로그인 담당 이벤트 루프
        self.account_event_loop = QEventLoop()
        self.calculator_event_loop = QEventLoop()
        self.calculator_event_loop = QEventLoop() # 조건검색 이벤트 루프

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
        self.screen_my_account = "1000"
        self.screen_calculation_stock = "2000"

        # 초기 작업
        # self.create_kiwoom_instance()
        # self.event_collection()  # 이벤트와 슬롯을 메모리에 먼저 생성.
        # # self.login()
        # self.get_account_info()  # 계좌 번호만 얻어오기
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
        self.get_account_info()  # 계좌 번호만 얻어오기
        self.get_deposit_info()  # 예수금 관련된 정보 얻어오기
        self.get_account_evaluation_balance()  # 계좌평가잔고내역 얻어오기
        self.not_signed_account()  # 미체결내역 얻어오기
        self.calculator()

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
        
        # 조건검색식 관련
        self.OnReceiveConditionVer.connect(self.E_OnReceiveConditionVer)

    def get_account_info(self):
        account_list = self.dynamicCall("GetLoginInfo(QString)", "ACCNO")
        account_number = account_list.split(';')[0]
        self.account_number = account_number

    def get_deposit_info(self, nPrevNext=0):
        self.dynamicCall("SetInputValue(QString, QString)",
                         "계좌번호", self.account_number)
        self.dynamicCall("SetInputValue(QString, QString)", "비밀번호", " ")
        self.dynamicCall("SetInputValue(QString, QString)", "비밀번호입력매체구분", "00")
        self.dynamicCall("SetInputValue(QString, QString)", "조회구분", "2")
        self.dynamicCall("CommRqData(QString, QString, int, QString)",
                         "예수금상세현황요청", "opw00001", nPrevNext, self.screen_my_account)

        self.account_event_loop.exec_()

    def get_account_evaluation_balance(self, nPrevNext=0):
        self.dynamicCall("SetInputValue(QString, QString)",
                         "계좌번호", self.account_number)
        self.dynamicCall("SetInputValue(QString, QString)", "비밀번호", " ")
        self.dynamicCall("SetInputValue(QString, QString)", "비밀번호입력매체구분", "00")
        self.dynamicCall("SetInputValue(QString, QString)", "조회구분", "1")
        self.dynamicCall("CommRqData(QString, QString, int, QString)",
                         "계좌평가잔고내역요청", "opw00018", nPrevNext, self.screen_my_account)

        if not self.account_event_loop.isRunning():
            self.account_event_loop.exec_()

    def not_signed_account(self, nPrevNext=0):
        self.dynamicCall("SetInputValue(QString, QString)",
                         "계좌번호", self.account_number)
        self.dynamicCall("SetInputValue(QString, QString)", "전체종목구분", "0")
        self.dynamicCall("SetInputValue(QString, QString)", "매매구분", "0")
        self.dynamicCall("SetInputValue(QString, QString)", "체결구분", "1")
        self.dynamicCall("CommRqData(QString, QString, int, QString)",
                         "실시간미체결요청", "opt10075", nPrevNext, self.screen_my_account)

        if not self.account_event_loop.isRunning():
            self.account_event_loop.exec_()

    # -------------------------------------
    # 로그인 관련
    # -------------------------------------
    def login(self):
        self.dynamicCall("CommConnect()")  # 시그널 함수 호출.
        self.login_event_loop.exec_()

    # -------------------------------------
    # 로그인 상태 관련
    # -------------------------------------
    def login_connect_state(self):
        self.winLoginConnectState = LoginConnectStateWindow(self)
        self.winLoginConnectState.show()
        # os.system('cls')
        # isLogin = self.dynamicCall("GetConnectState()")
        # if isLogin == 1:
        #     print("\n현재 계정은 로그인 상태입니다.")
        # else:
        #     print("\n현재 계정은 로그아웃 상태입니다.")
        # input()

    # -------------------------------------
    # 사용자정보 조회
    # -------------------------------------
    def my_info(self):
        self.winMyInfoWindow = MyInfoWindow(self)
        self.winMyInfoWindow.show()
        # os.system('cls')
        # user_name = self.dynamicCall("GetLoginInfo(QString)", "USER_NAME")
        # user_id = self.dynamicCall("GetLoginInfo(QString)", "USER_ID")
        # account_count = self.dynamicCall(
        #     "GetLoginInfo(QString)", "ACCOUNT_CNT")
        #
        # print(f"\n이름 : {user_name}")
        # print(f"ID : {user_id}")
        # print(f"보유 계좌 수 : {account_count}")
        # print(f"계좌번호 : {self.account_number}")
        # input()

    # -------------------------------------
    # 예수금 조회
    # -------------------------------------
    def deposit_info(self):
        self.winDepositInfoWindow = DepositInfoWindow(self)
        self.winDepositInfoWindow.show()
        # os.system('cls')
        # print(f"\n예수금 : {self.deposit}원")
        # print(f"출금 가능 금액 : {self.withdraw_deposit}원")
        # print(f"주문 가능 금액 : {self.order_deposit}원")
        # input()

    # -------------------------------------
    # 평가금액 정보
    # -------------------------------------
    def account_evaulation_balance_info(self):
        self.winAccountBalanceInfoWindow = AccountBalanceInfoWindow(self)
        self.winAccountBalanceInfoWindow.show()
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
        self.conditionSearchWindow = ConditionSearchWindo(self)
        self.conditionSearchWindow.show()
        pass



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
    def E_OnReceiveTrData(self, sScrNo, sRQName, sTrCode, sRecordName, sPrevNext):
        if sRQName == "예수금상세현황요청":
            deposit = self.dynamicCall(
                "GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "예수금")
            self.deposit = int(deposit)

            withdraw_deposit = self.dynamicCall(
                "GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "출금가능금액")
            self.withdraw_deposit = int(withdraw_deposit)

            order_deposit = self.dynamicCall(
                "GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "주문가능금액")
            self.order_deposit = int(order_deposit)
            self.cancel_screen_number(self.screen_my_account)
            self.account_event_loop.exit()

        elif sRQName == "계좌평가잔고내역요청":
            if (self.total_buy_money == None or self.total_evaluation_money == None
                    or self.total_evaluation_profit_and_loss_money == None or self.total_yield == None):
                total_buy_money = self.dynamicCall(
                    "GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "총매입금액")
                self.total_buy_money = int(total_buy_money)

                total_evaluation_money = self.dynamicCall(
                    "GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "총평가금액")
                self.total_evaluation_money = int(total_evaluation_money)

                total_evaluation_profit_and_loss_money = self.dynamicCall(
                    "GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "총평가손익금액")
                self.total_evaluation_profit_and_loss_money = int(
                    total_evaluation_profit_and_loss_money)

                total_yield = self.dynamicCall(
                    "GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "총수익률(%)")
                self.total_yield = float(total_yield)

            cnt = self.dynamicCall(
                "GetRepeatCnt(QString, QString)", sTrCode, sRQName)

            for i in range(cnt):
                stock_code = self.dynamicCall(
                    "GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "종목번호")
                stock_code = stock_code.strip()[1:]

                stock_name = self.dynamicCall(
                    "GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "종목명")
                stock_name = stock_name.strip()  # 필요 없는 공백 제거.

                stock_evaluation_profit_and_loss = self.dynamicCall(
                    "GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "평가손익")
                stock_evaluation_profit_and_loss = int(
                    stock_evaluation_profit_and_loss)

                stock_yield = self.dynamicCall(
                    "GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "수익률(%)")
                stock_yield = float(stock_yield)

                stock_buy_money = self.dynamicCall(
                    "GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "매입가")
                stock_buy_money = int(stock_buy_money)

                stock_quantity = self.dynamicCall(
                    "GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "보유수량")
                stock_quantity = int(stock_quantity)

                stock_trade_quantity = self.dynamicCall(
                    "GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "매매가능수량")
                stock_trade_quantity = int(stock_trade_quantity)

                stock_present_price = self.dynamicCall(
                    "GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "현재가")
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

            if sPrevNext == "2":
                self.get_account_evaluation_balance(2)
            else:
                self.cancel_screen_number(self.screen_my_account)
                self.account_event_loop.exit()

        elif sRQName == "실시간미체결요청":
            cnt = self.dynamicCall(
                "GetRepeatCnt(QString, QString)", sTrCode, sRQName)

            for i in range(cnt):
                stock_code = self.dynamicCall(
                    "GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "종목코드")
                stock_code = stock_code.strip()

                stock_order_number = self.dynamicCall(
                    "GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "주문번호")
                stock_order_number = int(stock_order_number)

                stock_name = self.dynamicCall(
                    "GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "종목명")
                stock_name = stock_name.strip()

                stock_order_type = self.dynamicCall(
                    "GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "주문구분")
                stock_order_type = stock_order_type.strip().lstrip('+').lstrip('-')

                stock_order_price = self.dynamicCall(
                    "GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "주문가격")
                stock_order_price = int(stock_order_price)

                stock_order_quantity = self.dynamicCall(
                    "GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "주문수량")
                stock_order_quantity = int(stock_order_quantity)

                stock_not_signed_quantity = self.dynamicCall(
                    "GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "미체결수량")
                stock_not_signed_quantity = int(stock_not_signed_quantity)

                stock_signed_quantity = self.dynamicCall(
                    "GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "체결량")
                stock_signed_quantity = int(stock_signed_quantity)

                stock_present_price = self.dynamicCall(
                    "GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "현재가")
                stock_present_price = int(
                    stock_present_price.strip().lstrip('+').lstrip('-'))

                stock_order_status = self.dynamicCall(
                    "GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "주문상태")
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

            if sPrevNext == "2":
                self.not_signed_account(2)
            else:
                self.cancel_screen_number(sScrNo)
                self.account_event_loop.exit()

        elif sRQName == "주식일봉차트조회요청":
            stock_code = self.dynamicCall(
                "GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "종목코드")
            #six_hundred_data = self.dynamicCall("GetCommDataEx(QString, QString)", sTrCode, sRQName)

            stock_code = stock_code.strip()
            cnt = self.dynamicCall(
                "GetRepeatCnt(QString, QString)", sTrCode, sRQName)  # 최대 600일

            for i in range(cnt):
                calculator_list = []

                current_price = self.dynamicCall(
                    "GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "현재가")
                volume = self.dynamicCall(
                    "GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "거래량")
                trade_price = self.dynamicCall(
                    "GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "거래대금")
                date = self.dynamicCall(
                    "GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "일자")
                start_price = self.dynamicCall(
                    "GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "시가")
                high_price = self.dynamicCall(
                    "GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "고가")
                low_price = self.dynamicCall(
                    "GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "저가")

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

            if sPrevNext == "2":
                self.day_kiwoom_db(stock_code, None, 2)
            else:
                self.calculator_event_loop.exit()

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

    """
        getConditionLoad() 메서드의 조건식 목록 요청에 대한 응답 이벤트
        
        :param receive: int - 응답결과(1: 성공, 나머지 실패)
        :param msg: string - 메세지
    """
    def E_OnReceiveConditionVer(self, receive, msg):
        try:
            if not receive:
                return

            self.condition = self.getConditionNameList()
            print("조건식 개수: ", len(self.condition))

            for key in self.condition.keys():
                print("조건식: ", key, ": ", self.condition[key])
                # print("key type: ", type(key))

        except Exception as e:
            print(e)

        finally:
            self.calculator_event_loop.exit()
        # pass

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

    def cancel_screen_number(self, sScrNo):
        self.dynamicCall("DisconnectRealData(QString)", sScrNo)


    def get_code_list_by_market(self, market_code):
        code_list = self.dynamicCall(
            "GetCodeListByMarket(QString)", market_code)
        code_list = code_list.split(";")[:-1]
        return code_list

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
        # self.dynamicCall("SetInputValue(QString, QString)", "종목코드", stock_code)
        # self.dynamicCall("SetInputValue(QString, QString)", "수정주가구분", 1)
        #
        # if date != None:  # date가 None일 경우 date는 오늘 날짜 기준
        #     self.dynamicCall("SetInputValue(QString, QString)", "기준일자", date)
        #
        # self.dynamicCall("CommRqData(QString, QString, int, QString)",
        #                  "주식일봉차트조회요청", "opt10081", nPrevNext, self.screen_calculation_stock)
        #
        # if not self.calculator_event_loop.isRunning():
        #     self.calculator_event_loop.exec_()