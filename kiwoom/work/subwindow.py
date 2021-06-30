from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QHBoxLayout, QPushButton

class SubWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Sub Window')
        self.setGeometry(100, 100, 200, 100)
        layout = QVBoxLayout()
        layout.addStretch(1)
        edit = QLineEdit()
        font = edit.font()
        font.setPointSize(20)
        edit.setFont(font)
        self.edit = edit
        subLayout = QHBoxLayout()

        btnOK = QPushButton("확인")
        btnOK.clicked.connect(self.onOKButtonClicked)
        btnCancel = QPushButton("취소")
        btnCancel.clicked.connect(self.onCancelButtonClicked)
        layout.addWidget(edit)

        subLayout.addWidget(btnOK)
        subLayout.addWidget(btnCancel)
        layout.addLayout(subLayout)
        layout.addStretch(1)
        self.setLayout(layout)

    def onOKButtonClicked(self):
        self.accept()

    def onCancelButtonClicked(self):
        self.reject()

    def showModal(self):
        return super().exec_()