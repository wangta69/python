import sys
from PyQt5.QtWidgets import *
from KiwoomAPI import *

class KiwoonMain:
    def __init__(self):
        self.app = QApplication(sys.argv)  # QApplication 객체 생성.
        self.kiwoom = KiwoomAPI()
        self.kiwoom.CommConnect() # 로그인 처리
        self.GetLoginInfo() # 로그인 정보 호출
        self.OPT10001() # 실시간 처리
        self.app.exec_()  # 이벤트 루프 실행.
    
    # 로그인 정보
    def GetLoginInfo(self):
        print('GetLoginInfo start')
        # 로그인 상태
        self.kiwoom.GetConnectState()

        # 로그인 정보
        self.kiwoom.GetLoginInfo("ACCOUNT_CNT")
        self.kiwoom.GetLoginInfo("ACCLIST")
        self.kiwoom.GetLoginInfo("USER_ID")
        self.kiwoom.GetLoginInfo("USER_NAME")
        self.kiwoom.GetLoginInfo("KEY_BSECGB")
        self.kiwoom.GetLoginInfo("FIREW_SECGB")
        self.kiwoom.GetLoginInfo("GetServerGubun")

    # TR 목록
    def OPT10001(self):
        print('OPT10001 start')
        self.kiwoom.output_list = ['종목명']

        self.kiwoom.SetInputValue("종목코드", "005930")
        self.kiwoom.CommRqData("OPT10001", "OPT10001", 0, "0101")
        print(self.kiwoom.ret_data)
        return self.kiwoom.ret_data

if __name__ == "__main__":
    KiwoonMain()
    # app = QApplication(sys.argv)
    # api_con = KiwoonMain()
    #
    # result = api_con.GetLoginInfo()
    # app.exec_()