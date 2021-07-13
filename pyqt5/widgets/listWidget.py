import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic

# referer : https://wikidocs.net/35477

form_class = uic.loadUiType("list.widget.ui")[0]

class WindowClass(QMainWindow, form_class) :
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # ListWidget의 시그널
        self.listWidget.itemClicked.connect(self.chkItemClicked)
        self.listWidget.itemDoubleClicked.connect(self.chkItemDoubleClicked)
        self.listWidget.currentItemChanged.connect(self.chkCurrentItemChanged)

        # 버튼에 기능 연결
        self.btn_addItem.clicked.connect(self.addListWidget)
        self.btn_insertItem.clicked.connect(self.insertListWidget)

        self.btn_printItem.clicked.connect(self.printCurrentItem)
        self.btn_printMultiItems.clicked.connect(self.printMultiItems)
        self.btn_removeItem.clicked.connect(self.removeCurrentItem)
        self.btn_clearItem.clicked.connect(self.clearItem)

    # ListWidget의 시그널에 연결된 함수들
    def chkItemClicked(self):
        print(self.listWidget.currentItem().text())

    def chkItemDoubleClicked(self):
        print(str(self.listWidget.currentRow()) + " : " + self.listWidget.currentItem().text())

    def chkCurrentItemChanged(self):
        print("Current Row : " + str(self.listWidget.currentRow()))

    # 항목을 추가, 삽입하는 함수들
    def addListWidget(self):
        self.addItemText = self.line_addItem.text()
        self.listWidget.addItem(self.addItemText)

    def insertListWidget(self):
        self.insertRow = self.spin_insertRow.value()
        self.insertText = self.line_insertItem.text()
        self.listWidget.insertItem(self.insertRow, self.insertText)

    # Button Function
    def printCurrentItem(self):
        if self.listWidget.currentItem():
            print(self.listWidget.currentItem().text())

    def printMultiItems(self):
        # 여러개를 선택했을 때, selectedItems()를 이용하여 선택한 항목을 List의 형태로 반환받습니다.
        # 그 후, for문을 이용하여 선택된 항목을 출력합니다.
        # 출력할 때, List안에는 QListWidgetItem객체가 저장되어 있으므로, .text()함수를 이용하여 문자열로 변환해야 합니다.
        self.selectedList = self.listWidget.selectedItems()
        for i in self.selectedList :
            print(i.text())

    def removeCurrentItem(self):
        # ListWidget에서 현재 선택한 항목을 삭제할 때는 선택한 항목의 줄을 반환한 후, takeItem함수를 이용해 삭제합니다.
        self.removeItemRow = self.listWidget.currentRow()
        self.listWidget.takeItem(self.removeItemRow)

    def clearItem(self):
        self.listWidget.clear()

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()