import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QFont, QColor
from PyQt5 import uic

form_class = uic.loadUiType("comboBox.ui")[0]

# referer : https://wikidocs.net/35493

class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        #프로그램 실행 시 두개의 ComboBox를 동기화시키는 코드
        self.syncComboBox()

        #ComboBox에 기능 연결
        self.comboBox.currentIndexChanged.connect(self.comboBoxFunction)

        #버튼에 기능 연결
        self.btn_printItem.clicked.connect(self.printComboBoxItem)
        self.btn_clearItem.clicked.connect(self.clearComboBoxItem)
        self.btn_addItem.clicked.connect(self.addComboBoxItem)
        self.btn_deleteItem.clicked.connect(self.deleteComboBoxItem)

    def syncComboBox(self) :
        for i in range(0, self.comboBox.count()):
            self.comboBox_2.addItem(self.comboBox.itemText(i))

    def comboBoxFunction(self):
        self.lbl_display.setText(self.comboBox.currentText())

    def clearComboBoxItem(self):
        self.comboBox.clear()
        self.comboBox_2.clear()

    def printComboBoxItem(self) :
        print(self.comboBox_2.currentText())

    def addComboBoxItem(self) :
        self.comboBox.addItem(self.lineedit_addItem.text())
        self.comboBox_2.addItem(self.lineedit_addItem.text())
        print("Item Added")

    def deleteComboBoxItem(self):
        self.delidx = self.comboBox_2.currentIndex()
        self.comboBox.removeItem(self.delidx)
        self.comboBox_2.removeItem(self.delidx)
        print("Item Deleted")

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()