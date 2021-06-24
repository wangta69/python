import sys
import datetime
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *

dt_now = datetime.datetime.now()

COM_CODE = "005930" # 삼성전자
COM_DATE = dt_now.strftime('%Y%m%d') # 기준일자 600 거래일 전일 부터 현제까지 받아옴
# COM_DATE = "20190516" # 기준일자 600 거래일 전일 부터 현제까지 받아옴
print(COM_DATE)

class KiwoomAPIWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyStock")
        self.setGeometry(300, 300, 300, 500)

        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.kiwoom.CommConnect()


        self.kiwoom.OnEventConnect.connect(self.event_connect)
        # Tran 수신시 이벤트
        self.kiwoom.OnReceiveTrData.connect(self.receive_trdata)

        # TextEdit 생성
        self.text_edit = QTextEdit(self)
        self.text_edit.setGeometry(0, 0, 200, 200)
        self.text_edit.setEnabled(False)

        # 버튼 생성
        btn1 = QPushButton("조회", self)
        btn1.setGeometry(0, 202, 200, 60)
        btn1.clicked.connect(self.btn1_clicked)



    def btn1_clicked(self):
        self.callStockPrice()

    def callStockPrice(self):
        # 파라미터 세팅
        print(COM_DATE)
        self.kiwoom.SetInputValue("종목코드", COM_CODE)
        self.kiwoom.SetInputValue("기준일자", COM_DATE)
        self.kiwoom.SetInputValue("수정주가구분", "0")
        # sRQName, sTrCode, nPrevNext, sScreenNo
        res = self.kiwoom.CommRqData("opt10081_주가조회", "opt10081", 0, "10081")
        if res == 0:
            print('주가 요청 성공!!!!!!' + str(res))
        else:
            print('주가 요청 실패 !!!!!!' + str(res))

        # res = self.kiwoom.CommRqData("일별데이터조회", "OPT10086", 0, "0001") # 처음조회시 혹은 연속데이터가 없을때
        # if res == 0:
        #     print('주가 요청 성공!!!!!!' + str(res))
        # else:
        #     print('주가 요청 실패 !!!!!!' + str(res))
        #
        # res = self.kiwoom.CommRqData("일별데이터조회", "OPT10086", 2, "0001") # 연속조회시
        # if res == 0:
        #     print('주가 요청 성공!!!!!!' + str(res))
        # else:
        #     print('주가 요청 실패 !!!!!!' + str(res))

    # CallBack 함수
    def event_connect(self, nErrCode):
        if nErrCode == 0:
            self.text_edit.append("Login Success")

    # CallBack 함수
    def receive_trdata(self, sScrNo, sRQName, sTrCode, sRecordName, sPreNext, nDataLength, sErrorCode, sMessage, sSplmMsg):
        print('sRQName:')
        print(sRQName)
        if sRQName == "opt10081_주가조회":
            dataCount = self.kiwoom.GetRepeatCnt(sTrCode, sRQName)
            print('총 데이터 수 : ', dataCount)
            code = self.kiwoom.GetCommData(sTrCode, sRQName, 0, "종목코드")
            print("종목코드: " + code)
            print("------------------------------")
            # 가장최근에서 10 거래일 전까지 데이터 조회
            for dataIdx in range(0, 10):
                inputVal = ["일자", "거래량", "시가", "고가", "저가", "현재가"]
                outputVal = ['', '', '', '', '', '']
                for idx, j in enumerate(inputVal):
                    outputVal[idx] = self.kiwoom.GetCommData(sTrCode, sRQName, dataIdx, j)

                for idx, output in enumerate(outputVal):
                    print(inputVal[idx] + output)
                print('----------------')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    kaWindow = KiwoomAPIWindow()
    kaWindow.show()
    app.exec_()