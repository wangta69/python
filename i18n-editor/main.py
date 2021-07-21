import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic

import subprocess
import webbrowser

form_class = uic.loadUiType("main.ui")[0]

class MainWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self) # 현재 form_class를 선택한다.
        self.set_action()


    def set_action(self):
        self.menu_new_project_json.triggered.connect(self.new_project)

    def new_project(self):
        print('new_project')
        # path = "C:/Users/Username/PycharmProjects"
        # path = ''
        # webbrowser.open(path)  # Opens 'PycharmProjects' folder.

        subprocess.Popen(r'explorer /select,"C:\path\of\folder\file"')
        pass

if __name__ == "__main__":

    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
