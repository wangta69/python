import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from connMysql import Mysql
import datetime

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
        pass
        # self.tableWidget.setItem(0, 0, QTableWidgetItem("(0,0)"))
        # self.tableWidget.setItem(0, 1, QTableWidgetItem("(0,1)"))
        # self.tableWidget.setItem(1, 0, QTableWidgetItem("(1,0)"))
        # self.tableWidget.setItem(1, 1, QTableWidgetItem("(1,1)"))

    def btn_list_clicked(self):
        # QMessageBox.about(self, "message", "검색완료")
        # self.tableWidget.resize(500, 500)
        # self.tableWidget.setColumnCount(5)
        self.setTableWidgetData()

        #조회
        rows = self.mysql.selectTableList()
        self.tableWidget.setRowCount(len(rows))
        count = 0;
        for row in rows:
            # print(row[0], row[1], row[2], row[3])
            print(row)
            self.tableWidget.setItem(count, 0, QTableWidgetItem(str(row[0])))
            self.tableWidget.setItem(count, 1, QTableWidgetItem(row[1]))
            self.tableWidget.setItem(count, 2, QTableWidgetItem(row[2]))
            self.tableWidget.setItem(count, 3, QTableWidgetItem(row[3]))
            self.tableWidget.setItem(count, 4, QTableWidgetItem(row[4].strftime('%d/%m/%Y %H:%M:%S')))
            count += 1

    def btn_add_clicked(self):
        QMessageBox.about(self, "message", "추가")
        self.mysql.insertTable(
            self.input_name.text(),
            self.input_subject.text(),
            self.input_content.text()
        )

        #조회
        rows = self.mysql.selectTableList()
        self.tableWidget.setRowCount(len(rows))
        count  = 0;
        for row in rows:
            # print(row[0], row[1], row[2], row[3])
            self.tableWidget.setItem(count, 0, QTableWidgetItem(str(row[0])))
            self.tableWidget.setItem(count, 1, QTableWidgetItem(row[1]))
            self.tableWidget.setItem(count, 2, QTableWidgetItem(row[2]))
            self.tableWidget.setItem(count, 3, QTableWidgetItem(row[3]))
            count += 1

    def btn_delete_clicked(self):
        # QMessageBox.about(self, "message", "삭제")
        current = self.tableWidget.currentItem()
        print(current)
        if current is not None:
            txt = "row={0}, column={1}, content={2}".format(current.row(), current.column(), current.text())
        else:
            txt = "clicked cell = ({0},{1}) ==>None type<==".format(self.table.currentRow(), self.table.currentColumn())

        # selection = self.tableWidget.selectionModel()
        # indexes = selection.selectedRows()
        #
        # print(selection, indexes)

        index = self.tableWidget.selectedRanges()  # 1
        # index = index[0].bottomRow()
        # prin
        print(index[0][0])
        # self.tableWidget.removeRow(index[0])

        # msg = QMessageBox.information(self, 'cell 내용', txt)
        # QModelIndexList indexes = ui->tableWidget->selectionModel()->selectedRows();
        # for (int i = indexes.count() - 1; i >= 0; i--)
        # {
        #     ui->tableWidget->removeRow(indexes.at(i).row());
        # }

        # indexes = self.tableWidget.selectedRows()
        # columns = range(self.tableWidget.columnCount())
        # for index in indexes:
        #     row = index.row()
        #     print([index.sibling(row, c).data() for c in columns])




        # self.mysql.deleteTable(10)
        # aa = self.tableWidget.selectedIndexes()
        # print(aa)
        # cell = set((idx.row(), idx.column()) for idx in aa)
        # print(cell)
        # txt1 = "selected cells ; {0}".format(cell)
        # msg = QMessageBox.information(self, 'selectedIndexes()...', txt1)



        #조회
        rows = self.mysql.selectTableList()
        self.tableWidget.setRowCount(len(rows))
        count  = 0;
        for row in rows:
            # print(row[0], row[1], row[2], row[3])
            self.tableWidget.setItem(count, 0, QTableWidgetItem(str(row[0])))
            self.tableWidget.setItem(count, 1, QTableWidgetItem(row[1]))
            self.tableWidget.setItem(count, 2, QTableWidgetItem(row[2]))
            self.tableWidget.setItem(count, 3, QTableWidgetItem(row[3]))
            count += 1


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()

# insertTable( 10, 'abc', '010-9999-9999','etceee')
# updateTable('bbe',10)

