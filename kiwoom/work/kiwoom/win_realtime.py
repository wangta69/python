from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5 import uic
from PyQt5.QtGui import QStandardItemModel, QStandardItem

import re
from connMysql import Mysql
from utils.trie import Trie

from kiwoom.worker import Worker

form_class = uic.loadUiType("ui/kiwoom/realtime.ui")[0]


class RealtimeWindow(QWidget, form_class):
    def __init__(self, kiwoom=None):
        super().__init__()
        self.kiwoom = kiwoom
        self.isLogin = kiwoom.is_login()
        self.setupUi(self)  # 현재 form_class를 선택한다.

        self.lineEdit.textEdited.connect(self.line_edit_text_changed)
        self.listView.clicked.connect(self.listview_item_clicked)
        self.realtimeData.clicked.connect(self.realtime_data_clicked)

        self.mysql = Mysql()
        self.trie = Trie()

        self.insert_keyword()

        # self.set_kiwoom_api()  # connect to kiwoom COM Object
        # self.set_event_slot()
        self.ret_data = {}
        self.output_list = []

        self.worker = Worker()
        self.worker.signal_on_receive_real_data.connect(self.signal_slot)

        # print('self.kiwoom.user_signal', self.kiwoom.user_signal)

    # noinspection PyMethodMayBeStatic
    def signal_slot(self, tr_code, real_type, real_data):
        print('signal_slot', tr_code, real_type, real_data)
        pass

    def opt10001(self, code):
        """
        주식기본정보요청
        :param code:
        :return:
        """
        if self.isLogin != 1:
            QMessageBox.about(self, 'Alert', "먼저 로그인 해 주세요")
            pass
        else:
            self.output_list = ['종목명']
            self.kiwoom.SetInputValue("종목코드", code)
            self.kiwoom.comm_rq_data("종목정보요청", "opt10001", 0, "0101")

    def insert_keyword(self):
        """
        검색용 키워드를 미리 입력해 둔다.
        :return:
        """
        corporations = self.mysql.corporations()

        for row in corporations:
            self.trie.insert(row['comp_name'] + '(' + row['code'] + ')')

    def line_edit_text_changed(self):
        text = self.lineEdit.text()
        result = self.trie.starts_with(text)
        model = QStandardItemModel()
        if result and len(text) >= 1:
            for f in result:
                model.appendRow(QStandardItem(f))
        self.listView.setModel(model)

    def listview_item_clicked(self, index):
        text = self.listView.model().data(index)
        # regex = "\(.*\)|\s-\s.*"
        regex = r'\([^)]*\)'
        text = re.sub(regex, '', text)
        self.lineEdit.setText(text)

    def realtime_data_clicked(self):
        # 클릭시 실시간 차트 가져오기
        # 종목코드를 가져온다.
        comp_name = self.lineEdit.text()
        print('realtimeDataClicked', comp_name)
        if comp_name:
            code = self.mysql.codeFromCompName(comp_name)
            if code:
                self.opt10001(code)
        pass
