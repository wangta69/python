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

# referer : https://kminito.tistory.com/36

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
        # self.listWidget.itemClicked.connect(self.chkItemClicked)
        self.listWidget.itemDoubleClicked.connect(self.chkItemClicked)

        # 이벤트 루프 관련 변수
        self.condition_serarch_event_loop = QEventLoop()  # 조건검색 이벤트 루프
        self.OnReceiveTrCondition.connect(self.receiveTrCondition)
        self.OnReceiveRealCondition.connect(self.receiveRealCondition)

        # 조건검색식 관련 (GetConditionLoad())
        self.kiwoom.OnReceiveConditionVer.connect(self.E_OnReceiveConditionVer)

        # self.mysql = Mysql()
        # self.condition = ''
        self.getConditionLoad()

    def getConditionLoad(self):
        print("[getConditionLoad]")
        """ 조건식 목록 요청 메서드 """

        isLoad = self.kiwoom.dynamicCall("GetConditionLoad()")
        # 요청 실패시
        if not isLoad:
            print("getConditionLoad(): 조건식 요청 실패")

    def chkItemClicked(self):
        print('chkItemClicked')
        print(str(self.listWidget.currentRow()) + " : " + self.listWidget.currentItem().text())
        text = self.listWidget.currentItem().text()
        # print(self.condition)

        reverse_dic = dict(map(reversed, self.condition.items()))
        conditionIndex = reverse_dic[text]
        print('====', text, conditionIndex)
        self.sendCondition('0', text, conditionIndex, 0)

    """
        BSTR screenNo,    // 화면번호
        BSTR conditionName,  // 조건식 이름
        int conditionIndex,     // 조건명 인덱스
        int isRealTime   // 조회구분, 0:조건검색, 1:실시간 조건검색
    """
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

        isRequest = self.kiwoom.dynamicCall("SendCondition(QString, QString, int, int",
                                     screenNo, conditionName, conditionIndex, isRealTime)

        if not isRequest:
            print("sendCondition(): 조건검색 요청 실패")

        receiveTrCondition() # 이벤트 메서드에서 루프 종료

        self.condition_serarch_event_loop.exec_()

    def sendConditionStop(self, screenNo, conditionName, conditionIndex):
        print("[sendConditionStop]")
        """ 종목 조건검색 중지 메서드 """

        self.kiwoom.dynamicCall("SendConditionStop(QString, QString, int)", screenNo, conditionName, conditionIndex)

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
                self.listWidget.addItem(self.condition[key])

        except Exception as e:
            print(e)

        finally:
            self.condition_serarch_event_loop.exit()
        # pass

    def getConditionNameList(self):
        print("[getConditionNameList]")
        """
        조건식 획득 메서드

        조건식을 딕셔너리 형태로 반환합니다.
        이 메서드는 반드시 receiveConditionVer() 이벤트 메서드안에서 사용해야 합니다.

        :return: dict - {인덱스:조건명, 인덱스:조건명, ...}
        """

        data = self.kiwoom.dynamicCall("GetConditionNameList()")

        if data == "":
            print("getConditionNameList(): 사용자 조건식이 없습니다.")

        conditionList = data.split(';')
        del conditionList[-1]

        conditionDictionary = {}

        for condition in conditionList:
            key, value = condition.split('^')
            conditionDictionary[int(key)] = value

        return conditionDictionary

    def receiveTrCondition(self, screenNo, codes, conditionName, conditionIndex, inquiry):
        """
        (1회성, 실시간) 종목 조건검색 요청시 발생되는 이벤트

        :param screenNo: string
        :param codes: string - 종목코드 목록(각 종목은 세미콜론으로 구분됨)
        :param conditionName: string - 조건식 이름
        :param conditionIndex: int - 조건식 인덱스
        :param inquiry: int - 조회구분(0: 남은데이터 없음, 2: 남은데이터 있음)
        """

        print("[receiveTrCondition]")
        try:
            if codes == "":
                return

            codeList = codes.split(';')
            del codeList[-1]

            print(codeList)
            print("종목개수: ", len(codeList))

        finally:
            self.conditionLoop.exit()



    def receiveRealCondition(self, code, event, conditionName, conditionIndex):
        print("[receiveRealCondition]")
        """
        실시간 종목 조건검색 요청시 발생되는 이벤트

        :param code: string - 종목코드
        :param event: string - 이벤트종류("I": 종목편입, "D": 종목이탈)
        :param conditionName: string - 조건식 이름
        :param conditionIndex: string - 조건식 인덱스(여기서만 인덱스가 string 타입으로 전달됨)
        """

        print("종목코드: {}, 종목명: {}".format(code, self.get_master_code_name(code)))
        print("이벤트: ", "종목편입" if event == "I" else "종목이탈")