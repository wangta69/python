from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QTableWidget, QTableWidgetItem
from beautifultable import BeautifulTable

class UncontractInfoWindow(QWidget):

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.initUI()

    def initUI(self):
        okButton = QPushButton('OK')
        okButton.clicked.connect(self.close)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(okButton)
        hbox.addStretch(1)



        # os.system('cls')
        # print()
        table = self.make_table()
        # if len(self.parent.not_signed_account_dict) == 0:
        #     print("미체결 내역이 없습니다!")
        # else:
        #     print(table)
        # input()

        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(2)
        self.tableWidget.setColumnCount(2)

        self.tableWidget.setItem(0, 0, QTableWidgetItem('Apple'))
        self.tableWidget.setItem(0, 1, QTableWidgetItem('Banana'))
        self.tableWidget.setItem(1, 0, QTableWidgetItem('Orange'))
        self.tableWidget.setItem(1, 1, QTableWidgetItem('Grape'))

        # layout = QVBoxLayout()
        # layout.addWidget(self.tableWidget)
        # self.setLayout(layout)
        #
        # self.setWindowTitle('PyQt5 - QTableWidget')
        # self.setGeometry(300, 100, 600, 400)
        # self.show()

        vbox = QVBoxLayout()
        vbox.addStretch(3)
        vbox.addLayout(hbox)
        vbox.addLayout(self.tableWidget)
        vbox.addStretch(1)

        self.setLayout(vbox)
        self.setWindowTitle('실시간미체결요청')
        self.setGeometry(300, 300, 300, 200)

    def make_table(self):
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(2)
        self.tableWidget.setColumnCount(2)

        self.tableWidget.setItem(0, 0, QTableWidgetItem('Apple'))
        self.tableWidget.setItem(0, 1, QTableWidgetItem('Banana'))
        self.tableWidget.setItem(1, 0, QTableWidgetItem('Orange'))
        self.tableWidget.setItem(1, 1, QTableWidgetItem('Grape'))

        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)
        self.setLayout(layout)

        self.setWindowTitle('PyQt5 - QTableWidget')
        self.setGeometry(300, 100, 600, 400)
        self.show()

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
