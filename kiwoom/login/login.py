import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QAxContainer import *


class KiwoomWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # self.setWindowTitle("Python 로그인")
        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.kiwoom.OnEventConnect.connect(self._handler_login)

        # login
        self.kiwoom.dynamicCall("CommConnect()")
        # self.login_loop = QEventLoop()
        # self.login_loop.exec()
        
        # account 입력창 보임
        # self.kiwoom.dynamicCall("KOA_Functions(QString, QString)", "ShowAccountWindow", "")

    def _handler_login(self, nErrCode):
        print(nErrCode)
        try:
            # self.login_loop.exit()
            self.event_loop_CommConnect.exit()
        except:
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = KiwoomWindow()
 #   win.show()
    app.exec_()