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

form_class = uic.loadUiType("ui/kiwoom/realtime.ui")[0]
class RealtimeWindow(QWidget, form_class):

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.isLogin = parent.dynamicCall("GetConnectState()")
        self.setupUi(self)  # 현재 form_class를 선택한다.

        self.lineEdit.textEdited.connect(self.lineeditTextChanged)
        self.listView.clicked.connect(self.listviewItemClicked)
        self.realtimeData.clicked.connect(self.realtimeDataClicked)

        self.mysql = Mysql()
        self.insertKeyword()

        # self.set_kiwoom_api()  # connect to kiwoom COM Object
        # self.set_event_slot()
        self.ret_data = {}
        self.output_list = []

        # TR 목록
    """
        주식기본정보요청
    """
    def OPT10001(self, code):
        print('OPT10001 start')
        if self.isLogin != 1:
            QMessageBox.about(self, 'Alert', "먼저 로그인 해 주세요")
            pass
        else:
            self.output_list = ['종목명']

            self.parent.SetInputValue("종목코드", code)
            self.parent.CommRqData("OPT10001", "OPT10001", 0, "0101")
        # return self.parent.ret_data

    """
        검색용 키워드를 미리 입력해 둔다.
    """
    def insertKeyword(self):
        corporations = self.mysql.corporations()
        self.trie = Trie()

        for row in corporations:
            self.trie.insert(row['comp_name'] + '(' + row['code'] + ')')

    def lineeditTextChanged(self):
        text = self.lineEdit.text()
        result = self.trie.starts_with((text))
        model = QStandardItemModel()
        if result and len(text) >= 1:
            for f in result:
                model.appendRow(QStandardItem(f))
        self.listView.setModel(model)

    def listviewItemClicked(self, index):
        text = self.listView.model().data(index)
        # regex = "\(.*\)|\s-\s.*"
        regex = r'\([^)]*\)'
        text = re.sub(regex, '', text)
        self.lineEdit.setText(text)

    def realtimeDataClicked(self):
        # 클릭시 실시간 차트 가져오기
        # 종목코드를 가져온다.
        comp_name = self.lineEdit.text()
        if comp_name:
            code = self.mysql.codeFromCompName(comp_name)
            if code:
                self.OPT10001(code)
        pass
