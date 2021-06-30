from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView
from beautifultable import BeautifulTable

# https://freeprog.tistory.com/333
class UncontractInfoWindow(QWidget):

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent

        self.tableWidget = QTableWidget(parent)

        self.createLayout()
        self.createTable()

    def createLayout(self):
        self.okButton = QPushButton('OK')
        self.okButton.clicked.connect(self.close)


        self.thbox = QHBoxLayout()
        self. thbox.addStretch(1)
        self.thbox.addWidget(self.tableWidget)
        self.thbox.addStretch(1)

        self.hbox = QHBoxLayout()
        self.hbox.addStretch(1)
        self. hbox.addWidget(self.okButton)
        self.hbox.addStretch(1)


        self.vbox = QVBoxLayout()
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.thbox)
        self.vbox.addLayout(self.hbox)
        # vbox.addLayout(self.tableWidget)
        self.vbox.addStretch(1)

        self.setLayout(self.vbox)
        self.setWindowTitle('실시간미체결요청')
        self.setGeometry(300, 300, 300, 200)

    def createTable(self):
        # self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(9)
        self.tableWidget.setRowCount(2)

        # column header 명 설정.
        self.tableWidget.setHorizontalHeaderLabels(["주문번호", "종목명", "주문구분", "주문가격", "주문수량", "미체결수량", "체결량", "현재가", "주문상태"])
        self.tableWidget.horizontalHeaderItem(0).setToolTip("코드...") # header tooltip
        # self.table.horizontalHeaderItem(0).setTextAlignment(Qt.AlignRight) # header 정렬 방식

        i = 0
        j = 0
        for stock_order_number in self.parent.not_signed_account_dict:
            i = i + 1
            j = 0

            stock = self.not_signed_account_dict[stock_order_number]
            stockList = [stock_order_number]
            for key in stock:
                j = j + 1
                self.tableWidget.setItem(i, j, QTableWidgetItem('Apple'))
                self.tableWidget.setItem(i, j, QTableWidgetItem('Banana'))
                self.tableWidget.setItem(i, j, QTableWidgetItem('Orange'))
                self.tableWidget.setItem(i, j, QTableWidgetItem('Grape'))
        #         output = None
        #         if key == "주문가격" or key == "현재가":
        #             output = str(stock[key]) + "원"
        #         elif '량' in key:
        #             output = str(stock[key]) + "개"
        #         elif key == "종목코드":
        #             continue
        #         else:
        #             output = stock[key]
        #         stockList.append(output)
        #     table.rows.append(stockList)



        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 위젯크기에 맞게

    # def make_table(self):
    #     self.tableWidget = QTableWidget()
    #     self.tableWidget.setRowCount(2)
    #     self.tableWidget.setColumnCount(2)
    #
    #     self.tableWidget.setItem(0, 0, QTableWidgetItem('Apple'))
    #     self.tableWidget.setItem(0, 1, QTableWidgetItem('Banana'))
    #     self.tableWidget.setItem(1, 0, QTableWidgetItem('Orange'))
    #     self.tableWidget.setItem(1, 1, QTableWidgetItem('Grape'))
    #
    #     layout = QVBoxLayout()
    #     layout.addWidget(self.tableWidget)
    #     self.setLayout(layout)
    #
    #     self.setWindowTitle('PyQt5 - QTableWidget')
    #     self.setGeometry(300, 100, 600, 400)
    #     self.show()

    # def make_table(self):
    #     # table = BeautifulTable()
    #     table = BeautifulTable(maxwidth=150)
    #
    #     for stock_order_number in self.parent.not_signed_account_dict:
    #         stock = self.not_signed_account_dict[stock_order_number]
    #         stockList = [stock_order_number]
    #         for key in stock:
    #             output = None
    #             if key == "주문가격" or key == "현재가":
    #                 output = str(stock[key]) + "원"
    #             elif '량' in key:
    #                 output = str(stock[key]) + "개"
    #             elif key == "종목코드":
    #                 continue
    #             else:
    #                 output = stock[key]
    #             stockList.append(output)
    #         table.rows.append(stockList)
    #     table.columns.header = ["주문번호", "종목명", "주문구분", "주문가격", "주문수량",
    #                             "미체결수량", "체결량", "현재가", "주문상태"]
    #     table.rows.sort('주문번호')
    #     return table
