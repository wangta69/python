import sys
import os
import easygui
import tkinter as tk
from tkinter import filedialog
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
        self.dir = ''


    def set_action(self):
        self.menu_new_project_json.triggered.connect(self.new_project)
        self.actionImport_Project.triggered.connect(self.import_project)
        self.actionAdd_Locale.triggered.connect(self.add_locale)

    def new_project(self):
        root = tk.Tk()
        root.withdraw()

        # files = filedialog.askopenfilenames()

        dir = filedialog.askdirectory()
        self.getMeta(dir)


        # explorer would choke on forward slashes
        # path = ''
        # FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')
        # path = os.path.normpath(path)
        #
        # if os.path.isdir(path):
        #     subprocess.run([FILEBROWSER_PATH, path])
        # elif os.path.isfile(path):
        #     subprocess.run([FILEBROWSER_PATH, '/select,', path])

        # file = easygui.fileopenbox()

        # path of the current script
        # path = 'D:/Pycharm projects/gfg'
        #
        # # Before creating
        # dir_list = os.listdir(path)
        # print("List of directories and files before creation:")
        # print(dir_list)
        # print()
        #
        # # Creates a new file
        # with open('myfile.txt', 'w') as fp:
        #     pass
        #     # To write data to new file uncomment
        #     # this fp.write("New file created")
        #
        # # After creating
        # dir_list = os.listdir(path)
        # print("List of directories and files after creation:")
        # print(dir_list)
        #
        # print('new_project')
        # path = "C:/Users/Username/PycharmProjects"
        # path = ''
        # webbrowser.open(path)  # Opens 'PycharmProjects' folder.

        # subprocess.Popen(r'explorer /select,"C:\path\of\folder\file"')


        # f = open("demofile2.txt", "a")
        # f.write("Now the file has more content!")
        # f.close()
        #
        # # open and read the file after the appending:
        # f = open("demofile2.txt", "r")
        # print(f.read())

        pass

    def import_project(self):
        self.dir = filedialog.askdirectory()
        pass

    def add_locale(self):
        print('add project', self.dir);

        myvar = easygui.enterbox("Enter locale(i.e en_US):")
        if myvar != None:
            # create folder and translations.json file
            local_dir = self.dir + '\\' + myvar;
            os.mkdir(local_dir)

            f = open(local_dir + '\\translations.json', "a")
            f.write("{\n")
            f.write("}\n")
            f.close()

            pass
        else:
            print('pass')
            pass
        pass

    def getMeta(self, metapath):
        file = metapath + '\\.i18n-editor-metadata'
        print(file)
        if os.path.isfile(file):
            print("Yes. it is a file")
        elif os.path.isdir(file):
            print("Yes. it is a directory")
        elif os.path.exists(file):
            print("Something exist")
        else:
            f = open(file, "a")
            f.write("minify_resources=0\n")
            f.write("resource_type=JSON\n")
            f.write("resource_name=translations\n")
            f.close()


if __name__ == "__main__":

    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
