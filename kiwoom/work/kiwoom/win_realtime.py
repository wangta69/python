from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5 import uic
from PyQt5.QAxContainer import *
from PyQt5.QtCore import QEventLoop
from beautifultable import BeautifulTable

form_class = uic.loadUiType("ui/kiwoom/realtime.ui")[0]
class RealtimeWindow(QWidget, form_class):

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setupUi(self)  # 현재 form_class를 선택한다.

        # self.set_kiwoom_api()  # connect to kiwoom COM Object
        # self.set_event_slot()
        self.ret_data = {}
        self.output_list = []

        # TR 목록

        self.OPT10001()

    def OPT10001(self):
        print('OPT10001 start')
        self.output_list = ['종목명']

        self.parent.SetInputValue("종목코드", "005930")
        self.parent.CommRqData("OPT10001", "OPT10001", 0, "0101")
        # return self.parent.ret_data

    # # COM 오브젝트 생성.
    # def set_kiwoom_api(self):
    #     self.setControl("KHOPENAPI.KHOpenAPICtrl.1")
    #
    # def set_event_slot(self):
    #     # 공통
    #     # self.parent.OnReceiveMsg.connect(self.E_OnReceiveMsg)
    #
    #     # 로그인 버전처리
    #     # self.OnEventConnect.connect(self.E_OnEventConnect)
    #
    #     # 조회와 실시간 데이터 처리
    #     self.parent.OnReceiveTrData.connect(self.E_OnReceiveTrData)
    #     self.parent.OnReceiveRealData.connect(self.E_OnReceiveRealData)
    #
    # # ========== #
    # ### Event 함수 ###
    # ## 공통 ##
    # def E_OnReceiveMsg(self, sScrNo, sRQName, sTrCode, sMsg):
    #     print(sScrNo, sRQName, sTrCode, sMsg)
    #
    # ## 로그인 버전처리 ##
    # def E_OnEventConnect(self, nErrCode):
    #     print(nErrCode)
    #     self.event_loop_CommConnect.exit()
    #
    # ## 조회와 실시간 데이터 처리 ##
    # def E_OnReceiveTrData(self, sScrNo, sRQName, sTrCode, sRecordName, sPrevNext, nDataLength, sErrorCode, sMessage,
    #                       sSplmMsg):
    #     print(sScrNo, sRQName, sTrCode, sRecordName, sPrevNext, nDataLength, sErrorCode, sMessage, sSplmMsg)
    #
    #     self.Call_TR(sTrCode, sRQName)
    #
    #     self.event_loop_CommRqData.exit()
    #
    # def E_OnReceiveRealData(self, sCode, sRealType, sRealData):
    #     print(sCode, sRealType, sRealData)
    #
    # # ========== #
    # ### OpenAPI 함수 ###
    # ## 로그인 버전처리 ##
    # # 로그인
    # def CommConnect(self):
    #     self.dynamicCall('CommConnect()')
    #     self.event_loop_CommConnect = QEventLoop()
    #     self.event_loop_CommConnect.exec_()
    #
    # # 로그인 상태
    # def GetConnectState(self):
    #     ret = self.dynamicCall('GetConnectState()')
    #
    #     print(ret)
    #
    # def GetLoginInfo(self, kind=''):
    #     ret = self.dynamicCall('GetLoginInfo(String)', kind)
    #     print(ret)
    #
    # ## 조회와 실시간 데이터 처리 ##
    # # 조회 요청
    # def CommRqData(self, sRQName, sTrCode, nPrevNext, sScreenNo):
    #     ret = self.dynamicCall('CommRqData(String, String, int, String)', sRQName, sTrCode, nPrevNext, sScreenNo)
    #     self.event_loop_CommRqData = QEventLoop()
    #     self.event_loop_CommRqData.exec_()
    #
    #     # print(ret)
    #
    # # 조회 요청 시 TR의 Input 값을 지정
    # def SetInputValue(self, sID, sValue):
    #     ret = self.dynamicCall('SetInputValue(String, String)', sID, sValue)
    #
    # # 조회 수신한 멀티 데이터의 개수(Max : 900개)
    # def GetRepeatCnt(self, sTrCode, sRecordName):
    #     ret = self.dynamicCall('GetRepeatCnt(String, String)', sTrCode, sRecordName)
    #
    #     # print(ret)
    #     return ret
    #
    # # 조회 데이터 요청
    # def GetCommData(self, strTrCode, strRecordName, nIndex, strItemName):
    #     ret = self.dynamicCall('GetCommData(String, String, int, String)', strTrCode, strRecordName, nIndex,
    #                            strItemName)
    #
    #     # print(ret)
    #     return ret.strip()
    #
    # # ========== #
    # # TR 요청
    # def Call_TR(self, strTrCode, sRQName):
    #     self.ret_data[strTrCode] = {}
    #     self.ret_data[strTrCode]['Data'] = {}
    #
    #     self.ret_data[strTrCode]['TrCode'] = strTrCode
    #
    #     count = self.GetRepeatCnt(strTrCode, sRQName)
    #     self.ret_data[strTrCode]['Count'] = count
    #
    #     if count == 0:
    #         temp_list = []
    #         temp_dict = {}
    #         for output in self.output_list:
    #             data = self.GetCommData(strTrCode, sRQName, 0, output)
    #             temp_dict[output] = data
    #
    #         temp_list.append(temp_dict)
    #
    #         self.ret_data[strTrCode]['Data'] = temp_list
    #
    #     if count >= 1:
    #         temp_list = []
    #         for i in range(count):
    #             temp_dict = {}
    #             for output in self.output_list:
    #                 data = self.GetCommData(strTrCode, sRQName, i, output)
    #                 temp_dict[output] = data
    #
    #             temp_list.append(temp_dict)
    #
    #         self.ret_data[strTrCode]['Data'] = temp_list
