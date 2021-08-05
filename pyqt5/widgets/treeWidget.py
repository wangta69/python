import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5 import uic
from PyQt5.QtWidgets import QTreeWidgetItem

form_class = uic.loadUiType("tree.widget.ui")[0]

# referer : https://stackoverflow.com/questions/57180377/how-can-i-save-the-file-in-treeview-as-a-json-file-again
# https://www.python2.net/questions-454829.htm

class WindowClass(QMainWindow, form_class) :
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # self.treeWidget.setText(0, 'Fruit')

        # item = QTreeWidgetItem()
        # item.setText(0, "Fruit")
        # item.setText(1, "Apple")
        #
        # self.treeWidget.addChild(item)

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

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()