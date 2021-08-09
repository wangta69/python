import json
import argparse
from sys import exit as sysExit
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidget, QFileDialog, QDockWidget, QAction, QTreeWidgetItem
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
    def __init__(self, parent):
        QTreeWidget.__init__(self)
        self.MyParent = parent
        self.TreeRoot = self.invisibleRootItem()
   # Just to show you what a static method looks like
   # one that does not need a reference to self because
   # it does not use self -- non-essential you can
   # delete this when you are done testing with it
    @staticmethod
    def PrintTree():
        print('Tree View Ready')
    def FillTree(self):
        def new_item(parent, text, val=None):
            child = QTreeWidgetItem([text])
            child.setFlags(child.flags() | Qt.ItemIsEditable)
            fill_item(child, val)
            parent.addChild(child)
            child.setExpanded(True)
        if self.JSonTable is None:
            pass
        elif isinstance(self.JSonTable, dict):
            for key, val in sorted(self.JSonTable.items()):
                new_item(self.TreeRoot, str(key), val)
        elif isinstance(self.JSonTable, (list, tuple)):
            for val in self.JSonTable:
                text = (str(val) if not isinstance(val, (dict, list, tuple))
                        else '[%s]' % type(val).__name__)
                new_item(self.TreeRoot, text, val)
        else:
            new_item(self.TreeRoot, str(self.JSonTable))
   # This is meant to capture the On Change Event for the QTreeWidget
    def OnChange(self):
        print('Handling Changes Here for:',self.MyParent.JSonTable)
      # This routine would update your JsonTable with any changes
      # that take place within your TreeWidget however I do not
      # think this is the correct function name to capture that
      # event so you might have to research this one a bit to get
      # the appropriate name
class MainWindow(QMainWindow):
    def __init__(self, JsonFilePath):
        super(MainWindow, self).__init__()
        self.setWindowTitle('Json File Editor')
        self.setGeometry(300, 100, 900, 600)
        self.JsonFile = JsonFilePath
        self.JSonTable = None
        self.CenterPane = ViewTree(self)
        self.setCentralWidget(self.CenterPane)
        self.CenterPane.PrintTree()
# Rem'd out because I could not test this for you
# However it should work or... it might need tweaks
#        if len(self.JsonFile) > 0:
#            self.LoadFile()
        self.MainMenu = MenuToolBar(self)
    def OpenFile():
        self.JsonFile = QFileDialog.getOpenFileName()
      # Do not recall if QFileDialog returns None or not so you need to check that
        if len(self.JsonFile) > 0:
            self.LoadFile()
    def LoadFile():
      # Note one should always validate that they have a valid file prior to opening it
      # isfile() -- and checking the file extension are two methods I use
        JsonData = open(self.JsonFile[0],"r")
        self.JSonTable = json.load(JsonData)
        self.CenterPane.FillTree(self.JSonTable)
    def SaveFile():
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