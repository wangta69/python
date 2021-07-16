from PyQt5.QtCore import QEventLoop
from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5 import uic

from kiwoom.worker import Worker

form_class = uic.loadUiType("ui/kiwoom/condition.search.ui")[0]

# referer : https://kminito.tistory.com/36

"""
(1) GetConditionLoad 실행 (조건검색 목록 요청)
GetConditionLoad 실행 -> 서버에서 응답이 오면 OnReceiveConditionVer 실행-> OnReceiveConditionVer 안에서 GetConditionNameList 실행되며 등록된 조건검색식 목록 출력

(2) SendCondition 실행 (조건검색 요청 - 위에서 찾은 조건 검색식 번호 및 이름 전달)
SendCondition 실행 -> 서버에서 응답이 오면 OnReceiveTrCondition 실행되며 해당 조건 검색 결과 표시(종목 코드)
-> (SendCondition 실시간 요청시) 해당 조건 검색 결과에 변동이 있을 경우 OnReceiveRealCondition 실행되어 실시간으로 종목 편입/이탈 결과 출력
"""
class ConditionSearchWindow(QWidget, form_class):

    def __init__(self, kiwoom=None):
        super().__init__()
        self.setupUi(self)  # 현재 form_class를 선택한다.

        self.kiwoom = kiwoom
        self.isLogin = kiwoom.is_login()

        # self.listWidget.itemClicked.connect(self.condition_item_clicked)
        self.listWidget.itemDoubleClicked.connect(self.condition_item_clicked)

        # 이벤트 루프 관련 변수
        self.condition_serarch_event_loop = QEventLoop()  # 조건검색 이벤트 루프

        # 조건검색식 관련 (GetConditionLoad())
        self.worker = Worker()
        self.worker.signal_receive_condition_ver.connect(self.signal_ver)
        self.worker.signal_receive_tr_condition.connect(self.signal_tr) # 1회성
        self.worker.signal_receive_real_condition.connect(self.signal_real) # 실시간
        # # 조건검색식 관련
        self.kiwoom.OnReceiveConditionVer.connect(self.worker.on_receive_condition_ver)
        self.kiwoom.OnReceiveTrCondition.connect(self.worker.on_receive_tr_condition)
        self.kiwoom.OnReceiveRealCondition.connect(self.worker.receive_real_condition)

        self.condition_load()

    def signal_ver(self, receive, msg):
        """
        getConditionLoad() 메서드의 조건식 목록 요청에 대한 응답 이벤트

        :param receive: int - 응답결과(1: 성공, 나머지 실패)
        :param msg: string - 메세지
        """
        try:
            if not receive:
                return

            self.condition = self.kiwoom.getConditionNameList()
            print("조건식 개수: ", len(self.condition))

            for key in self.condition.keys():
                print("조건식: ", key, ": ", self.condition[key])
                self.listWidget.addItem(self.condition[key])

        except Exception as e:
            print(e)

        finally:
            print('finally')
            # pass
            # self.condition_serarch_event_loop.exit()


    def signal_tr(self, screen_no, codes, condition_name, condition_index, inquiry):
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
        print('screen_no: ', screen_no, 'codes: ', codes, 'condition_name: ', condition_name, 'condition_index: ', condition_index, 'inquiry: ', inquiry)
        try:
            if codes == "":
                return

            codeList = codes.split(';')
            del codeList[-1]

            print(codeList)
            print("종목개수: ", len(codeList))

        finally:
            pass

    #
    #
    def signal_real(self, code, event, condition_name, condition_index):
        """
        실시간 종목 조건검색 요청시 발생되는 이벤트
        :param code: string - 종목코드
        :param event: string - 이벤트종류("I": 종목편입, "D": 종목이탈)
        :param condition_name: string - 조건식 이름
        :param condition_index: string - 조건식 인덱스(여기서만 인덱스가 string 타입으로 전달됨)
        :return:
        """
        print('signal_real')
        print('receive_real_condition', code, event, condition_name, condition_index)
        print("종목코드: {}, 종목명: {}".format(code, self.kiwoom.get_master_code_name(code)))
        print("이벤트: ", "종목편입" if event == "I" else "종목이탈")


    def condition_load(self):
        """
        조건식 목록 요청 메서드: 사용자가 만든 컨디션 목록을 가져온다.
        현재 창에 접근시 자동실행
        :return:
        """
        if self.isLogin != 1:
            QMessageBox.about(self, 'Alert', "먼저 로그인 해 주세요")
            pass
        else:
            print('condition_load GetConditionLoad start')
            isLoad = self.kiwoom.dynamicCall("GetConditionLoad()")  # OnReceiveConditionVer

            print('condition_load GetConditionLoad End')
            # 요청 실패시
            if not isLoad:
                QMessageBox.about(self, 'Alert', "조건식 요청 실패")

            # self.condition_serarch_event_loop.exec_()


    def condition_item_clicked(self):
        """
        현재 조건검색을 선택
        :return:
        """
        print('chkItemClicked')
        print(str(self.listWidget.currentRow()) + " : " + self.listWidget.currentItem().text())
        text = self.listWidget.currentItem().text()
        # print(self.condition)

        reverse_dic = dict(map(reversed, self.condition.items()))
        conditionIndex = reverse_dic[text]
        print('====', text, conditionIndex)
        self.kiwoom.send_condition('0', text, conditionIndex, 1)





