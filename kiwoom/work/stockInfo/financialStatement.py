from PyQt5.QtWidgets import QWidget, QTableWidgetItem
from PyQt5 import uic
import pandas as pd
from .financialStatementCrawling import Crawling
from connMysql import Mysql

form_class = uic.loadUiType("ui/stockinfo/finance.ui")[0]

class FinancialStatements(QWidget, form_class):
    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)  # 현재 form_class를 선택한다.
        self.LoadDataAction.clicked.connect(self.LoadDataClicked)
        self.CrawlingDataction.clicked.connect(self.CrawlingDataClicked)
        self.SavetoExcelAction.clicked.connect(self.SavetoExcelActionClicked)
        self.mysql = Mysql()

    def loadData(self):
        rows = self.mysql.financeinfos()
        self.tableWidget.setRowCount(len(rows))
        count = 0;
        for row in rows:
            # print(row[0], row[1], row[2], row[3])
            self.tableWidget.setItem(count, 0, QTableWidgetItem(str(row[0])))
            self.tableWidget.setItem(count, 1, QTableWidgetItem(row[1]))
            self.tableWidget.setItem(count, 2, QTableWidgetItem(row[2]))
            self.tableWidget.setItem(count, 3, QTableWidgetItem(str(row[3])))
            self.tableWidget.setItem(count, 4, QTableWidgetItem(str(row[4])))

            # 증가율 구하기
            if row[3] == 0:
                q1 = 1
            else:
                q1 = row[3]
            increaseRate = (row[4] - row[3]) / abs(q1)
            self.tableWidget.setItem(count, 5, QTableWidgetItem(str(round(increaseRate, 2))))

            # 흑전 구하기
            if row[3] < 0 and row[4] >= 0:
                self.tableWidget.setItem(count, 6, QTableWidgetItem('흑전'))
            else:
                self.tableWidget.setItem(count, 6, QTableWidgetItem('-'))
                
            # self.tableWidget.setItem(count, 4, QTableWidgetItem(row[4].strftime('%d/%m/%Y %H:%M:%S')))
            # self.tableWidget.setItem(count, 5, QTableWidgetItem('[update]'))
            count += 1

        # self.tableWidget.doubleClicked.connect(self.tableWidget_doubleClicked)
        # self.tableWidget.clicked.connect(self.tableWidget_Clicked)
    """
        저장된 데이타 호출하기
    """
    def LoadDataClicked(self):
        self.loadData()
        pass

    """
        클릭시 데이타를 크롤링한다.
    """
    def CrawlingDataClicked(self):
        crawling = Crawling()
        crawling.start()
        pass

    def SavetoExcelActionClicked(self):
        print('SavetoExcelActionClicked')
        columnHeaders = []

        # create column header list
        for j in range(self.tableWidget.model().columnCount()):
            columnHeaders.append(self.tableWidget.horizontalHeaderItem(j).text())

        df = pd.DataFrame(columns=columnHeaders)

        # create dataframe object recordset
        for row in range(self.tableWidget.rowCount()):
            for col in range(self.tableWidget.columnCount()):
                df.at[row, columnHeaders[col]] = self.tableWidget.item(row, col).text()

        df.to_excel('financialStatement.xlsx', index=False)

    # def SavetoExcelActionClicked(self):
    #     print('SavetoExcelActionClicked')
    #     raw_data = {
    #         'col0': [1, 2, 3, 4],
    #         'col1': [10, 20, 30, 40],
    #         'col2': [100, 200, 300, 400]
    #     }  # 리스트 자료형으로 생성
    #     raw_data = pd.DataFrame(raw_data)  # 데이터 프레임으로 전환
    #     raw_data.to_excel(excel_writer='sample.xlsx')  # 엑셀로 저장
