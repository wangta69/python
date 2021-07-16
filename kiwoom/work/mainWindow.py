from PyQt5.QtWidgets import QMainWindow, qApp
# from PyQt5 import QtWidgets
from PyQt5 import uic
from kiwoom.kiwoom import Kiwoom
from stockinfo.foreigner import Foreigner
from stockinfo.financialStatement import FinancialStatements
from stockinfo.listedCorporation import ListedCorporation

from help.platformInfo import PlatformInfoWindow
from subwindow import SubWindow

form_class = uic.loadUiType("ui/main.ui")[0]
class MainWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self) # 현재 form_class를 선택한다.
        self.kiwoom = Kiwoom(MainWindow)
        self.foreigner = Foreigner(MainWindow)
        self.initUI()

    def initUI(self):
        # self.setWindowTitle('Main Window')
        # _translate = QCoreApplication.translate
        # self.resize(800, 600)
        #

        # # Kiwoom > menu
        self.loginAction.triggered.connect(self.kiwoom.connect)
        self.loginStatusAction.triggered.connect(self.kiwoom.login_connect_state)
        self.userInfoAction.triggered.connect(self.kiwoom.my_info)
        self.depositInfoAction.triggered.connect(self.kiwoom.deposit_info)
        self.accountBalanceInfoAction.triggered.connect(self.kiwoom.account_evaulation_balance_info)
        self.unContractedInfoAction.triggered.connect(self.kiwoom.uncontract_info)
        self.realtimeDataAction.triggered.connect(self.kiwoom.realtime)
        self.conditionSearchAction.triggered.connect(self.kiwoom.conditionSearch)
        self.traderAction.triggered.connect(self.kiwoom.trader)
        self.kiwoomTestaction.triggered.connect(self.kiwoom.order)


        # 자료
        self.foreignerPlatformAction.triggered.connect(self.foreigner.info)
        self.financialStaPlatformAction.triggered.connect(self.financialThread)
        self.listedCorporationAction.triggered.connect(self.listedCorporation)


        # File
        self.exitAction.triggered.connect(qApp.quit)
        self.openAction.triggered.connect(self.onButtonClicked)

        # # Help
        self.menuHelpPlatform.triggered.connect(self.helpPlatformClicked)

        # Status Bar
        self.statusBar().showMessage('Not connected')

    def listedCorporation(self):
        self.listedCorporation = ListedCorporation(self)
        self.listedCorporation.show()

    def financialThread(self):
        self.financialStatement = FinancialStatements(self)
        self.financialStatement.show()

        # win = FinancialStatements()
        # win.show()
        # r = win.showModal()
       ## self.financialStatement.start()
        # self.financialStatement.expecting

    # Help > Platform
    def helpPlatformClicked(self):
        win = PlatformInfoWindow()
        win.show()

    def onButtonClicked(self):
        win = SubWindow()
        r = win.showModal()
        if r:
            text = win.edit.text()
            self.label.setText(text)

    def keyPressEvent(self, e):
        print('keyPressEvent from mainWindow', e)

    # def show(self):
    #     super().show()


