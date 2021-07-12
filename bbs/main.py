import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from connMysql import Mysql
import datetime

# referer : https://wikidocs.net/35498
# referer : https://gogosong.tistory.com/entry/QT-Desinger-%EC%9C%BC%EB%A1%9C-UI-%EA%B5%AC%EC%84%B1-%ED%95%98%EA%B3%A0-UI-%ED%8C%8C%EC%9D%BC%EC%9D%84-%ED%8C%8C%EC%9D%B4%EC%8D%AC-%EC%BD%94%EB%93%9C%EC%97%90%EC%84%9C-%EB%A1%9C%EB%93%9C%ED%95%98%EA%B8%B02%EC%A0%84%EC%B2%B4%EC%BD%94%EB%93%9C

form_class = uic.loadUiType("main_ui.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.mysql = Mysql()
        self.setupUi(self)
        self.btn_list.clicked.connect(self.btn_list_clicked)
        self.btn_add.clicked.connect(self.btn_add_clicked)
        self.btn_delete.clicked.connect(self.btn_delete_clicked)
        # self.tableWidget.itemDoubleClicked.connect(self.btn_delete_clicked)

        # self.tableWidget.resize(290, 290)
        # self.tableWidget.setRowCount(2)
        # self.tableWidget.setColumnCount(2)


    def setTableWidgetData(self):
        rows = self.mysql.selectTableList()
        self.tableWidget.setRowCount(len(rows))
        count = 0;
        for row in rows:
            # print(row[0], row[1], row[2], row[3])
            self.tableWidget.setItem(count, 0, QTableWidgetItem(str(row[0])))
            self.tableWidget.setItem(count, 1, QTableWidgetItem(row[1]))
            self.tableWidget.setItem(count, 2, QTableWidgetItem(row[2]))
            self.tableWidget.setItem(count, 3, QTableWidgetItem(row[3]))
            self.tableWidget.setItem(count, 4, QTableWidgetItem(row[4].strftime('%d/%m/%Y %H:%M:%S')))
            self.tableWidget.setItem(count, 5, QTableWidgetItem('[update]'))
            count += 1

        # self.tableWidget.doubleClicked.connect(self.tableWidget_doubleClicked)
        self.tableWidget.clicked.connect(self.tableWidget_Clicked)

    def btn_list_clicked(self):
        # QMessageBox.about(self, "message", "검색완료")
        # self.tableWidget.resize(500, 500)
        # self.tableWidget.setColumnCount(5)
        self.setTableWidgetData()


    def btn_add_clicked(self):
        # QMessageBox.about(self, "message", "추가")
        self.mysql.insertTable(
            self.input_name.text(),
            self.input_subject.text(),
            self.input_content.text()
        )

        self.setTableWidgetData()

    def btn_delete_clicked(self):
        # QMessageBox.about(self, "message", "삭제")
        # current = self.tableWidget.currentItem()
        current = self.tableWidget.currentRow()
        print('current', current)

        id = self.tableWidget.item(current, 0).text()
        self.mysql.deleteTable(id)

        self.setTableWidgetData()

    def tableWidget_Clicked(self):
        current = self.tableWidget.currentItem()
        print(current)
        column = current.column()
        print(column)
        if column == 5:
            row = self.tableWidget.currentRow()
            print(row)
            id = self.tableWidget.item(row, 0).text()
            name = self.tableWidget.item(row, 1).text()
            subject = self.tableWidget.item(row, 2).text()
            content = self.tableWidget.item(row, 3).text()
            print(id, name, subject, content)

            self.mysql.updateTable(id, name, subject, content)


        #  txt = "row={0}, column={1}, content={2}".format(aa.row(), aa.column(), aa.text())
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()

# updateTable('bbe',10)

