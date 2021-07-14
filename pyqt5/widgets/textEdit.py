import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QFont, QColor
from PyQt5 import uic

form_class = uic.loadUiType("textEdit.ui")[0]

class WindowClass(QMainWindow, form_class) :
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.fontSize = 10

        #TextEdit과 관련된 버튼에 기능 연결
        self.btn_printTextEdit.clicked.connect(self.printTextEdit)
        self.btn_clearTextEdit.clicked.connect(self.clearTextEdit)
        self.btn_setFont.clicked.connect(self.setFont)
        self.btn_setFontItalic.clicked.connect(self.fontItalic)
        self.btn_setFontColor.clicked.connect(self.fontColorRed)
        self.btn_fontSizeUp.clicked.connect(self.fontSizeUp)
        self.btn_fontSizeDown.clicked.connect(self.fontSizeDown)

    def printTextEdit(self):
        print(self.textEdit.toPlainText())

    def clearTextEdit(self):
        self.textEdit.clear()

    def setFont(self):
        fontvar = QFont('Apple SD Gothic Neo', 10)
        self.textEdit.setCurrentFont(fontvar)

    def fontItalic(self):
        self.textEdit.setFontItalic(True)

    def fontColorRed(self):
        colorvar = QColor(255, 0, 0)
        self.textEdit.setTextColor(colorvar)

    def fontSizeUp(self):
        self.fontSize = self.fontSize + 1
        self.textEdit.setFontPointSize(self.fontSize)

    def fontSizeDown(self):
        self.fontSize = self.fontSize - 1
        self.textEdit.setFontPointSize(self.fontSize)

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()