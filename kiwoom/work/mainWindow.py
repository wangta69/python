from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QStatusBar
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication
from work.kiwoom.kiwoom import Kiwoom
from work.stockInfo.foreigner import Foreigner
from work.stockInfo.financialStatement import FinancialStatements

from help.platformInfo import PlatformInfoWindow
from subwindow import SubWindow

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.kiwoom = Kiwoom(MainWindow)
        self.foreigner = Foreigner(MainWindow)
        self.financialStatement = FinancialStatements(MainWindow)

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Main Window')
        _translate = QCoreApplication.translate
        self.resize(800, 600)

        exitAction = QAction(QIcon('exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        openAction = QAction(QIcon('exit.png'), 'newWindow', self)
        openAction.triggered.connect(self.onButtonClicked)
        


        # Help
        helpPlatformAction = QAction(QIcon('exit.png'), 'platform', self)
        helpPlatformAction.triggered.connect(self.helpPlatformClicked)

        # Kiwoom > menu
        loginAction = QAction(QIcon('exit.png'), '접속 하기', self)
        loginAction.triggered.connect(self.kiwoom.connect)
        # loginAction.triggered.connect(self.kiwoom.login)

        loginStatusAction = QAction(QIcon('exit.png'), '접속 상태', self)
        loginStatusAction.triggered.connect(self.kiwoom.login_connect_state)

        userInfoAction = QAction(QIcon('exit.png'), '정보 조회', self)
        userInfoAction.triggered.connect(self.kiwoom.my_info)

        depositInfoAction = QAction(QIcon('exit.png'), '예수금 조회', self)
        depositInfoAction.triggered.connect(self.kiwoom.deposit_info)

        accountBalanceInfoAction = QAction(QIcon('exit.png'), '계좌 잔고 조회', self)
        accountBalanceInfoAction.triggered.connect(self.kiwoom.account_evaulation_balance_info)

        unContractedInfoAction = QAction(QIcon('exit.png'), '미체결 내역 조회', self)
        unContractedInfoAction.triggered.connect(self.kiwoom.uncontract_info)

        # 자료
        foreignerPlatformAction = QAction(QIcon('exit.png'), '외군인 한도 소진율 ', self)
        foreignerPlatformAction.triggered.connect(self.foreigner.info)

        financialStaPlatformAction = QAction(QIcon('exit.png'), '제무제표', self)
        # financialStaPlatformAction.triggered.connect(self.financialStatement.info)
        financialStaPlatformAction.triggered.connect(self.financialThread)

        menubar = self.menuBar()
        # Kiwoom > menu Add
        menuKiwoom = menubar.addMenu('&kiwoom')
        menuKiwoom.addAction(loginAction)
        menuKiwoom.addAction(loginStatusAction)
        menuKiwoom.addAction(userInfoAction)
        menuKiwoom.addAction(depositInfoAction)
        menuKiwoom.addAction(accountBalanceInfoAction)
        menuKiwoom.addAction(unContractedInfoAction)

        # StockInfo
        menuInform = menubar.addMenu('&StockInfo')
        menuInform.addAction(foreignerPlatformAction)
        menuInform.addAction(financialStaPlatformAction)

        # File
        # menubar.setNativeMenuBar(False)
        filemenu = menubar.addMenu('&File')
        filemenu.addAction(exitAction)
        filemenu.addAction(openAction)

        # Help
        helpmenu = menubar.addMenu('&Help')
        helpmenu.addAction(helpPlatformAction)

        MainWindow.statusBar = QStatusBar(self)
        self.setStatusBar(MainWindow.statusBar)
        self.statusBar.showMessage('Not connected')


    def financialThread(self):
        self.financialStatement.start()
        # self.financialStatement.expecting

    # Help > Platform
    def helpPlatformClicked(self):
        self.winPlatformInfo = PlatformInfoWindow()
        self.winPlatformInfo.show()
        # if r:
        #     text = win.edit.text()
        #     self.label.setText(text)

    def onButtonClicked(self):
        win = SubWindow()
        r = win.showModal()
        if r:
            text = win.edit.text()
            self.label.setText(text)

    def show(self):
        super().show()
