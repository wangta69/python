from PyQt5.QtWidgets import QWidget, QMessageBox, QPushButton, QHBoxLayout, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5 import uic
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QAxContainer import *
from PyQt5.QtCore import QEventLoop
from beautifultable import BeautifulTable

import re
from connMysql import Mysql
from utils.trie import Trie
from kiwoom.config.kiwoom import output_list
form_class = uic.loadUiType("ui/kiwoom/condition.search.ui")[0]


"""
(1) GetConditionLoad 실행 (조건검색 목록 요청)
GetConditionLoad 실행 -> 서버에서 응답이 오면 OnReceiveConditionVer 실행-> OnReceiveConditionVer 안에서 GetConditionNameList 실행되며 등록된 조건검색식 목록 출력

(2) SendCondition 실행 (조건검색 요청 - 위에서 찾은 조건 검색식 번호 및 이름 전달)
SendCondition 실행 -> 서버에서 응답이 오면 OnReceiveTrCondition 실행되며 해당 조건 검색 결과 표시(종목 코드)
-> (SendCondition 실시간 요청시) 해당 조건 검색 결과에 변동이 있을 경우 OnReceiveRealCondition 실행되어 실시간으로 종목 편입/이탈 결과 출력
"""
class ConditionSearchWindo(QWidget, form_class):

    def __init__(self, kiwoom=None):
        super().__init__()
        self.kiwoom = kiwoom
        self.isLogin = kiwoom.dynamicCall("GetConnectState()")
        self.setupUi(self)  # 현재 form_class를 선택한다.

        # self.lineEdit.textEdited.connect(self.lineeditTextChanged)
        # self.listView.clicked.connect(self.listviewItemClicked)
        # self.realtimeData.clicked.connect(self.realtimeDataClicked)

        self.mysql = Mysql()

        self.condition()
        # self.insertKeyword()
        #
        # # self.set_kiwoom_api()  # connect to kiwoom COM Object
        # # self.set_event_slot()
        # self.ret_data = {}
        # self.output_list = []

    """
        condition을 가져와서 display하기
    """
    def condition(self):
        # 조건식을 PC로 다운로드
        self.getConditionLoad()

        # 전체 조건식 리스트 얻기
        # conditions = self.kiwoom.GetConditionNameList()

        # print(conditions)
        # 0번 조건식에 해당하는 종목 리스트 출력
        # condition_index = conditions[0][0]
        # condition_name = conditions[0][1]
        # codes = self.kiwoom.SendCondition("0101", condition_name, condition_index, 0)
        #
        # print(codes)
        pass

    def getConditionLoad(self):
        print("[getConditionLoad]")
        """ 조건식 목록 요청 메서드 """

        isLoad = self.kiwoom.dynamicCall("GetConditionLoad()")
        # 요청 실패시
        if not isLoad:
            print("getConditionLoad(): 조건식 요청 실패")

        # receiveConditionVer() 이벤트 메서드에서 루프 종료
        self.kiwoom.conditionLoop = QEventLoop()
        self.kiwoom.conditionLoop.exec_()

    def sendCondition(self, screenNo, conditionName, conditionIndex, isRealTime):
        print("[sendCondition]")
        """
        종목 조건검색 요청 메서드

        이 메서드로 얻고자 하는 것은 해당 조건에 맞는 종목코드이다.
        해당 종목에 대한 상세정보는 setRealReg() 메서드로 요청할 수 있다.
        요청이 실패하는 경우는, 해당 조건식이 없거나, 조건명과 인덱스가 맞지 않거나, 조회 횟수를 초과하는 경우 발생한다.

        조건검색에 대한 결과는
        1회성 조회의 경우, receiveTrCondition() 이벤트로 결과값이 전달되며
        실시간 조회의 경우, receiveTrCondition()과 receiveRealCondition() 이벤트로 결과값이 전달된다.

        :param screenNo: string
        :param conditionName: string - 조건식 이름
        :param conditionIndex: int - 조건식 인덱스
        :param isRealTime: int - 조건검색 조회구분(0: 1회성 조회, 1: 실시간 조회)
        """

        isRequest = self.dynamicCall("SendCondition(QString, QString, int, int",
                                     screenNo, conditionName, conditionIndex, isRealTime)

        if not isRequest:
            print("sendCondition(): 조건검색 요청 실패")

        # receiveTrCondition() 이벤트 메서드에서 루프 종료
        self.kiwoom.calculator_event_loop = QEventLoop()
        self.kiwoom.calculator_event_loop.exec_()

    def sendConditionStop(self, screenNo, conditionName, conditionIndex):
        print("[sendConditionStop]")
        """ 종목 조건검색 중지 메서드 """

        self.kiwoom.dynamicCall("SendConditionStop(QString, QString, int)", screenNo, conditionName, conditionIndex)



    """
        주식기본정보요청
    """
    # def OPT10001(self, code):
    #     print('OPT10001 start')
    #     if self.isLogin != 1:
    #         QMessageBox.about(self, 'Alert', "먼저 로그인 해 주세요")
    #         pass
    #     else:
    #         self.output_list = ['종목명']
    #
    #         self.kiwoom.SetInputValue("종목코드", code)
    #         self.kiwoom.CommRqData("OPT10001", "OPT10001", 0, "0101")
    #     # return self.kiwoom.ret_data
    #
    # """
    #     검색용 키워드를 미리 입력해 둔다.
    # """
    # def insertKeyword(self):
    #     corporations = self.mysql.corporations()
    #     self.trie = Trie()
    #
    #     for row in corporations:
    #         self.trie.insert(row['comp_name'] + '(' + row['code'] + ')')
    #
    # def lineeditTextChanged(self):
    #     text = self.lineEdit.text()
    #     result = self.trie.starts_with((text))
    #     model = QStandardItemModel()
    #     if result and len(text) >= 1:
    #         for f in result:
    #             model.appendRow(QStandardItem(f))
    #     self.listView.setModel(model)
    #
    # def listviewItemClicked(self, index):
    #     text = self.listView.model().data(index)
    #     # regex = "\(.*\)|\s-\s.*"
    #     regex = r'\([^)]*\)'
    #     text = re.sub(regex, '', text)
    #     self.lineEdit.setText(text)
    #
    # def realtimeDataClicked(self):
    #     # 클릭시 실시간 차트 가져오기
    #     # 종목코드를 가져온다.
    #     comp_name = self.lineEdit.text()
    #     if comp_name:
    #         code = self.mysql.codeFromCompName(comp_name)
    #         if code:
    #             self.OPT10001(code)
    #     pass
