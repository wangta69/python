import json
from PyQt5.QtWidgets import *
import argparse
from sys import exit as sysExit

class MenuToolBar(QDockWidget):
    def __init__(self, MainWin):
        QDockWidget.__init__(self)
        self.MainWin = MainWin
        self.MainMenu = MainWin.menuBar()
        self.MenuActRef = {'OpnJsonAct':0,
                           'SavJsonAct':0}
        # ******* Create the File Menu *******
        self.FileMenu  = self.MainMenu.addMenu('File')
        # ******* Create File Menu Items *******
#        self.OpnJsonAct = QAction(QIcon('Images/open.ico'), '&Open', self)
        self.OpnJsonAct = QAction('&Open', self)
        self.OpnJsonAct.setShortcut("Ctrl+O")
        self.OpnJsonAct.setStatusTip('Open an Existing Json File')
        self.OpnJsonAct.triggered.connect(self.GetJsonFile)
        self.MenuActRef['OpnJsonAct'] = self.OpnJsonAct
#        self.SavJsonAct = QAction(QIcon('Images/save.ico'), '&Save', self)
        self.SavJsonAct = QAction('&Save', self)
        self.SavJsonAct.setShortcut("Ctrl+S")
        self.SavJsonAct.setStatusTip('Open an Existing Json File')
        self.SavJsonAct.triggered.connect(self.SaveJsonFile)
        self.MenuActRef['SavJsonAct'] = self.SavJsonAct
        # ******* Setup the File Menu *******
        self.FileMenu.addAction(self.OpnJsonAct)
        self.FileMenu.addSeparator()
        self.FileMenu.addAction(self.SavJsonAct)

    def GetJsonFile(self):
        self.MainWin.OpenFile()

    def SaveJsonFile(self):
        self.MainWin.SaveFile()


class ViewTree(QTreeWidget):
    def __init__(self, value):

        super().__init__()
        def fill_item(item, value):
            def new_item(parent, text, val=None):
                child = QTreeWidgetItem([text])
                fill_item(child, val)
                parent.addChild(child)
                child.setExpanded(True)
            if value is None: return
            elif isinstance(value, dict):
                for key, val in sorted(value.items()):
                    new_item(item, str(key), val)
            elif isinstance(value, (list, tuple)):
                for val in value:
                    text = (str(val) if not isinstance(val, (dict, list, tuple))
                            else '[%s]' % type(val).__name__)
                    new_item(item, text, val)
            else:
                new_item(item, str(value))

        fill_item(self.invisibleRootItem(), value)

class MainWindow(QMainWindow):
    def __init__(self, JsonFilePath):
        super(MainWindow, self).__init__()
        self.setWindowTitle('Json File Editor')
        self.setGeometry(300, 100, 900, 600)
        self.JsonFile = JsonFilePath
        self.JSonTable = None
        self.CenterPane = ViewTree(self)
        self.setCentralWidget(self.CenterPane)
        # self.CenterPane.PrintTree()
# Rem'd out because I could not test this for you
# However it should work or... it might need tweaks
#        if len(self.JsonFile) > 0:
#            self.LoadFile()
        self.MainMenu = MenuToolBar(self)

    def OpenFile(self):
        self.JsonFile = QFileDialog.getOpenFileName()
        # Do not recall if QFileDialog returns None or not so you need to check that
        if len(self.JsonFile) > 0:
            self.LoadFile()

    def LoadFile(self):
        print('LoadFile', self.JsonFile)
        # Note one should always validate that they have a valid file prior to opening it
        # isfile() -- and checking the file extension are two methods I use
        json_file = open(self.JsonFile[0], "r")
        print('json_file', json_file)
        self.file = json.load(json_file)
        print('file', self.file)
        ViewTree(self.file)
        # self.CenterPane.FillTree(self.file)

    def SaveFile(self):
        # Either to a new file or overwriting the exiting file
        # but basically you are now just saving your JsonTable
        # to file -- you could just loop through it manually or
        # I think there are wheels already invented to handle
        # Json objects like this and print them out to a file
        print('Saving Jason File')


def CmdLine():
    # create Parser object
    Parser = argparse.ArgumentParser(description = "Load this Json File - Given the full file path")
    # defining arguments for Parser object
    Parser.add_argument('-f', '--filepath', type = str, help = "This specifies the full path and filename for the Json File.")
    # parse the argument if any from standard input
    CmdLineVal = Parser.parse_args().filepath
    RetVal = ''
    if CmdLineVal != None:
        RetVal = CmdLineVal
    return RetVal


if __name__ == '__main__':
    JsonFilePath = CmdLine()
    MainThred = QApplication([])
    MainGUI = MainWindow(JsonFilePath)
    MainGUI.show()
    sysExit(MainThred.exec_())
    #
    # JsonFilePath = CmdLine()
    # app = QApplication([])
    #
    #
    # fname = QFileDialog.getOpenFileName()
    # json_file=open(fname[0],"r")
    # file=json.load(json_file)
    #
    #
    # window = ViewTree(file)
    # window.setGeometry(300, 100, 900, 600)
    # window.show()
    # app.exec_()
