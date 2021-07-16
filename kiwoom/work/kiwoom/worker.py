from PyQt5.QtCore import QObject, pyqtSignal
from .config.errCode import errors


class Worker(QObject):
    signal_test = pyqtSignal()
    signal_login = pyqtSignal()
    signal_on_receive_real_data = pyqtSignal(str, str, str)
    signal_on_receive_tr_data = pyqtSignal(str, str, str, str, str)

    signal_receive_condition_ver = pyqtSignal(int, str)
    signal_receive_tr_condition = pyqtSignal(str, str, str, int, int)
    signal_receive_real_condition = pyqtSignal(str, str, str, str)


    def test(self):
        print('signal_test')
        self.signal_test.emit()


    # noinspection PyMethodMayBeStatic
    def on_receive_message(self, src_no, rq_name, tr_code, msg):
        """

        :param src_no:
        :param rq_name:
        :param tr_code:
        :param msg:
        :return:
        """
        print('E_OnReceiveMsg', src_no, rq_name, tr_code, msg)
        pass

    # noinspection PyMethodMayBeStatic
    def on_event_connect(self, err_code):
        """
        로그인 버전처리
        :param err_code:
        :return:
        """
        print('E_OnEventConnect', err_code)
        if err_code == 0:
            print("로그인 성공")
        else:
            print("로그인 실패 - 에러 내용 :", errors(err_code)[1])
            # os.system('cls') # console 을 지울때 사용 'clear for linux and mac
            # sys.exit(0)

        self.signal_login.emit()

    # noinspection PyMethodMayBeStatic
    def on_receive_tr_data(self, src_no, rq_name, tr_code, record_name, prev_next):
        """
         :param src_no:
         :type src_no: str
         :type rq_name: str
         :type tr_code: str
         :type record_name: str
         :type prev_next: str
         """
        self.signal_on_receive_tr_data.emit(src_no, rq_name, tr_code, record_name, prev_next)

    # noinspection PyMethodMayBeStatic
    def on_receive_real_data(self, tr_code, real_type, real_data):
        """
        # 실시간으로 데이타 조회
        :param real_type: 주식예상체결, 장시작시간, 주식우선호가, 주식당일거래원
        :param real_data :
            주식우선호가: +79900	+79800
            주식예상체결: sRealData 152707	+79900	+200	+0.25	--212	715156	2
            주식체결: 153028	+79800	+100	+0.13	+79900	+79800	 774560	9700742	775794	+80000	+80200	+79800	2
            -67366	-3348496884	-99.31	0.16	208	70.86	4763886	2	0	-99.57	000000	000000	10022	090008	094034	153028	5101149
            3614467	-41.47	46716	28239	 61809888	 0	 0	 0	7980	6384	79973	425
            주식당일거래원: JP모간서울	1184351	+314738	033	DHDB	한  화	1038978	+24113	021	!!!!	이베스트	944407	+514	063	!!!! .....
            장시작시간 : 8	888888	000000
            장시작시간 : 2	152700	000300
        :type tr_code: str
        :type real_type: str
        :type real_data: str
        """
        print('sRealType', real_type)
        if real_type == '주식체결':
            print('sRealData', real_data)
            self.signal_on_receive_real_data.emit(tr_code, real_type, real_data)

    # 조건검색 관련시작
    def on_receive_condition_ver(self, receive, msg):
        """
        getConditionLoad() 메서드의 조건식 목록 요청에 대한 응답 이벤트

        :param receive: int - 응답결과(1: 성공, 나머지 실패)
        :param msg: string - 메세지
        """
        self.signal_receive_condition_ver.emit(receive, msg)

    def on_receive_tr_condition(self, screen_no, codes, condition_name, condition_index, inquiry):
        """
        (1회성, 실시간) 종목 조건검색 요청시 발생되는 이벤트
        :param screen_no:
        :type screen_no: str
        :param codes: - 종목코드 목록(각 종목은 세미콜론으로 구분됨)
        :param condition_name: 조건식 이름
        :type condition_name: str
        :param condition_index: 조건식 인덱스
        :type condition_index: int
        :param inquiry: 조회구분(0: 남은데이터 없음, 2: 남은데이터 있음)
        :type inquiry: int
        :return:
        """
        print('on_receive_tr_condition', screen_no, codes, condition_name, condition_index, inquiry)

        self.signal_receive_tr_condition.emit(screen_no, codes, condition_name, condition_index, inquiry)
        # self.conditionLoop.exit()

    def receive_real_condition(self, code, event, condition_name, condition_index):
        """
        실시간 종목 조건검색 요청시 발생되는 이벤트
        :param code: string - 종목코드
        :param event: string - 이벤트종류("I": 종목편입, "D": 종목이탈)
        :param condition_name: string - 조건식 이름
        :param condition_index: string - 조건식 인덱스(여기서만 인덱스가 string 타입으로 전달됨)
        :return:
        """
        self.signal_receive_real_condition.emit(code, event, condition_name, condition_index)
    # 조건검색 관련 끝