import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QTableWidget, QTableWidgetItem


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        okButton = QPushButton('OK')
        cancelButton = QPushButton('Cancel')

        tableWidget = QTableWidget()
        tableWidget.setRowCount(2)
        tableWidget.setColumnCount(2)

        tableWidget.setItem(0, 0, QTableWidgetItem('Apple'))
        tableWidget.setItem(0, 1, QTableWidgetItem('Banana'))
        tableWidget.setItem(1, 0, QTableWidgetItem('Orange'))
        tableWidget.setItem(1, 1, QTableWidgetItem('Grape'))

        thbox = QHBoxLayout()
        thbox.addStretch(1)
        thbox.addWidget(tableWidget)
        thbox.addStretch(1)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(okButton)
        hbox.addWidget(cancelButton)
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(thbox)
        vbox.addLayout(hbox)
        vbox.addStretch(1)

        self.setLayout(vbox)

        self.setWindowTitle('Box Layout')
        self.setGeometry(300, 300, 300, 200)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())