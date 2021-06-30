import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel
import platform
# from PyQt5.QtCore import QRect

class PlatformInfoWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        okButton = QPushButton('OK')
        okButton.clicked.connect(self.close)
    #    cancelButton = QPushButton('Cancel')

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(okButton)
     #   hbox.addWidget(cancelButton)
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(3)
        vbox.addLayout(hbox)
        vbox.addStretch(1)



        # label = QLabel(self.centralwidget)
        # self.label.setGeometry(QRect(120, 220, 71, 31))
        # self.label.setObjectName("label")


        self.setLayout(vbox)

        self.setWindowTitle('Platform Infomation')
        self.setGeometry(300, 300, 300, 200)

        platformarchi = platform.architecture()
        label = QLabel('', self)
        label.move(20, 20)
        # label.setGeometry(QRect(120, 220, 71, 31))
        #  label.setObjectName("label")
        label.setText(platformarchi[0] + ',' + platformarchi[1])

        print(platform.architecture())
    #
    # def close(self):
    #     print('close')


