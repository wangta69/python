import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QAbstractItemView
from PyQt5 import uic
from PyQt5.QtCore import Qt

form_class = uic.loadUiType("table.widget.ui")[0]

# referer : https://blog.naver.com/PostView.nhn?isHttpsRedirect=true&blogId=anakt&logNo=221834285100&parentCategoryNo=&categoryNo=14&viewDate=&isShowPopularPosts=false&from=postView
# https://freeprog.tistory.com/352

class WindowClass(QMainWindow, form_class) :
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.list = {
            '이세빈': {'학번': '20170001', '학부': '글로벌미디어', '번호': 1, '학점': 3.01, '숫자': 1111111},
            '김민수': {'학번': '20170001', '학부': '전가정보공학부', '번호': 3, '학점': 2.05, '숫자': 2222222},
            '홍길동': {'학번': '20170001', '학부': '소프트웨어학부', '번호': 12, '학점': -3.05, '숫자': 3333333},
            '이석준': {'학번': '20170001', '학부': '컴퓨터학부', '번호': 15, '학점': 3.33, '숫자': 4444}
        }
        self.sampleTable()

        # sorting 가능하게
        self.tableWidget.setSortingEnabled(True)
        # column header 명 설정.
        self.tableWidget.setHorizontalHeaderLabels(["이름", "학번", "학부", "번호", "학점", "숫자"])
        self.tableWidget.horizontalHeaderItem(0).setTextAlignment(Qt.AlignRight)  # header 정렬 방식

        self.tableWidget.verticalHeader().setVisible(False)  # 행번호 안나오게 하는 코드
        # self.tableWidget.horizontalHeader().setVisible(False)  # 열번호 안나오게 하는 코드
        self.tableWidget.setShowGrid(False)  # Table의 Grid를 보이지 않게 하는 코드
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)  # Row 단위 선택
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 셀 edit 금지




    def sampleTable(self):
        print(len(self.list))
        print(self.list)
        self.tableWidget.setRowCount(len(self.list))
        self.tableWidget.setColumnCount(6)
        count = 0
        for key in self.list:
            self.tableWidget.setItem(count, 0, QTableWidgetItem(key))
            self.tableWidget.setItem(count, 1, QTableWidgetItem(str(self.list[key]['학번'])))
            self.tableWidget.setItem(count, 2, QTableWidgetItem(str(self.list[key]['학부'])))

            번호 = QTableWidgetItem()
            번호.setData(Qt.DisplayRole, self.list[key]['번호'])
            self.tableWidget.setItem(count, 3, 번호)


            # self.tableWidget.setItem(count, 4, QTableWidgetItem(str(self.list[key]['학점'])))
            학점 = QTableWidgetItem()
            학점.setData(Qt.DisplayRole, self.list[key]['학점'])
            self.tableWidget.setItem(count, 4, 학점)

            숫자 = QTableWidgetItem()
            숫자.setData(Qt.DisplayRole, self.list[key]['숫자'])
            self.tableWidget.setItem(count, 5, 숫자)
            # self.tableWidget.setItem(count, 5, QTableWidgetItem('{:,}'.format(self.list[key]['숫자'])))

            self.tableWidget.item(count, 3).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tableWidget.item(count, 4).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tableWidget.item(count, 5).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

            count += 1

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()