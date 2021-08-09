import json
from collections import OrderedDict
import argparse
from sys import exit as sysExit
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidget, QFileDialog, QDockWidget, QAction, QTreeWidgetItem

# referer : https://www.python2.net/questions-454829.htm


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
        # self.TreeRoot = self.invisibleRootItem()
        self.JSonTable = ''
        # self.currentItemChanged.connect(self.handleCurrentItemChanged)
        self.itemChanged.connect(self.handleItemChanged)
        self.myItems = {}

    def fill_item(self, item, value):
        if value is None:
            pass
        elif isinstance(value, dict):
            for key, val in sorted(value.items()):
                self.new_item(item, str(key), val)
        elif isinstance(value, (list, tuple)):
            for val in value:
                text = (str(val) if not isinstance(val, (dict, list, tuple))
                        else '[%s]' % type(val).__name__)
                self.new_item(item, text, val)
        else:
            self.new_item(item, str(value))

    def new_item(self, parent, text, val=None):
        child = QTreeWidgetItem([text])
        child.setFlags(child.flags() | Qt.ItemIsEditable) # editable
        self.fill_item(child, val)
        # self.itemChanged.connect(self.itemChanged)
        # child.currentItemChanged.connect(self.itemChanged)

        parent.addChild(child)
        child.setExpanded(True)

    def generateString(self, treeItem):
        def getParent(item):
            if item.parent():
                global parents
                parents.append(str(item.parent().text(0)))
                getParent(item.parent())

        global parents
        parents = [str(treeItem.text(0))]
        getParent(treeItem)
        attribute, value = '.'.join(parents[::-1]), treeItem.text(1)
        return attribute, value

    def modelToDict(self):  # def modelToDict(self, parentItem = self.rootItem):
        '''Takes model presently in view, and saves all data as dictionary.
        Called by self.saveTodoData() and self.saveTodoDataAs()'''
        dictModel = {}
        # self.rootItem = self.nvisibleRootItem();
        print('self.TreeRoot', self.TreeRoot)
        # if self.TreeRoot.rowCount():

        for i in range(self.topLevelItemCount()):
            item = self.topLevelItem( i )
            dictModel["taskblocks"] = self.createTaskblockList(item)
            print('dictModel', dictModel);
        #
        # if self.topLevelItemCount():
        #     dictModel["taskblocks"] = self.createTaskblockList(self.topLevelItem())
        #     return dictModel

    def createTaskblockList(self, parentItem):
        '''Creates list of task blocks, and their tasks (latter using createTasklist).
        Called by modelToDict which is used to save the model as a dictionary'''
        numChildren = parentItem.rowCount()
        if numChildren:
            taskblockList = [None] * numChildren
            childList = self.getChildren(parentItem)
            for childNum in range(numChildren):
                childItem = childList[childNum]
                childTaskblockData = {}
                childTaskblockData["blockname"] = childItem.text()
                # now see if the block has children (tasks)
                if childItem.rowCount():
                    childTaskblockData["tasks"] = self.createTaskList(childItem)
                taskblockList[childNum] = childTaskblockData
            return taskblockList
        else:
            return None



    def listtoJSON(self, listItem):
        print('listtoJSON', listItem)
        for elem in listItem:
            print('elem[0]', elem[0], elem[1])
            if len(elem) > 1:
                 self.listtoJSON(elem[1])
            else:
                pass
        pass

    def get_subtree_nodes(self, tree_widget_item):
        """Returns all QTreeWidgetItems in the subtree rooted at the given node."""
        nodes = []
        nodes.append(tree_widget_item.text(0))
        for i in range(tree_widget_item.childCount()):
            # nodes.extend(self.get_subtree_nodes(tree_widget_item.child(i)))
            nodes.append(self.get_subtree_nodes(tree_widget_item.child(i)))
        return nodes

    def get_all_items(self):
        """Returns all QTreeWidgetItems in the given QTreeWidget."""
        all_items = []
        for i in range(self.topLevelItemCount()):
            top_item = self.topLevelItem(i)
            all_items.append(self.get_subtree_nodes(top_item))
            # all_items.extend(self.get_subtree_nodes(top_item))

        print('all_items', all_items)

        print('json.dumps', json.dumps(all_items))

        # self.listtoJSON(all_items)


        # d = {}
        # for elem in all_items[0]:
        #     print(elem)
        #     try:
        #         d[elem[1]].append(elem[0])
        #     except KeyError:
        #         d[elem[1]] = [elem[0]]



        # for ix in range(0, len(all_items)):
        #     print(all_items[ix].text(0))
        #     all_items[ix] = all_items[ix].text(0)
        # print('all_items', all_items)
        # return all_items
    # def get_subtree_nodes(self, tree_widget_item, all_item):
    #     """Returns all QTreeWidgetItems in the subtree rooted at the given node."""
    #     nodes = []
    #     nodes.append(tree_widget_item)
    #     if tree_widget_item.childCount():
    #         for i in range(tree_widget_item.childCount()):
    #             self.get_subtree_nodes(tree_widget_item.child(i), all_item)
    #     else:
    #         all_item = tree_widget_item.text(0)
    #         print('aaa', tree_widget_item.text(0))
    #     return tree_widget_item
    #
    # def get_all_items(self):
    #     """Returns all QTreeWidgetItems in the given QTreeWidget."""
    #     self.all_items = {}
    #     for i in range(self.topLevelItemCount()):
    #         top_item = self.topLevelItem(i)
    #         print('top_item', i, top_item.text(0))
    #         self.all_items[top_item.text(0)] = ''
    #         self.get_subtree_nodes(top_item, self.all_items[top_item.text(0)])
    #         # all_items.extend(self.get_subtree_nodes(top_item))
    #
    #     print('all_items', self.all_items)
    #     # for ix in range(0, len(all_items)):
    #     #     print(all_items[ix].text(0))
    #     #     all_items[ix] = all_items[ix].text(0)
    #     # print('all_items', all_items)
    #     # return all_items

    # This is meant to capture the On Change Event for the QTreeWidget
    def handleItemChanged(self, item, column):
        # print('item:', item, 'column', column, 'topLevelItemCount', self.topLevelItemCount())
        # dictModel = self.modelToDict()
        # print('dictModel', dictModel)


        self.get_all_items()

        # for i in range(self.topLevelItemCount()):
        #     item = self.topLevelItem( i )
        #
        #     count = item.childCount()
        #     # print('count', count, 'item.checkState(column)', item.checkState(column))
        #
        #     for index in range(count):
        #         it = item.child(index)
        #         # childItem.text()
        #         # print('item1', it)
        #         print('it.text()', it.text(0))
        #         url = it.text(0)  # text at first (0) column
        #         # print('url', it.text(0), it.text(1))
        #         attribute, value = self.generateString(it)
        #         print('attribute', attribute, 'value', value)
        #         # item.setText(1, 'result from %s' % url)  # update result column (1)



        # if item.checkState(column) == Qt.Checked:
        #     for index in range(count):
        #         item.child(index).setCheckState(0, Qt.Checked)
        # if item.checkState(column) == Qt.Unchecked:
        #     for index in range(count):
        #         item.child(index).setCheckState(0, Qt.Unchecked)

    def handleCurrentItemChanged(self, current, previous):
        print('Handling Changes Here for:', self.MyParent.JSonTable)
        print('current:', current, 'previous', previous)



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
        # self.CenterPane.itemChanged.connect(self.CenterPane.itemChanged)
        # self.CenterPane.PrintTree()
        # Rem'd out because I could not test this for you
        # However it should work or... it might need tweaks
        #        if len(self.JsonFile) > 0:
        #            self.LoadFile()
        self.MainMenu = MenuToolBar(self)

        # listitem = [['other', ['one', ['is 1']]], ['system', ['copiedasdfasdf', ['Copied.']], ['test', ['Test']]]]
        listitem = []
        listitem.append(['other', ['one', ['is 1']]])
        listitem.append(['system', ['copiedasdfasdf', ['Copied.']], ['test', ['Test']]])
        # self.CenterPane.listtoJSON(listitem)

    def OpenFile(self):
        self.JsonFile = QFileDialog.getOpenFileName()
        # Do not recall if QFileDialog returns None or not so you need to check that
        if len(self.JsonFile) > 0:
            self.LoadFile()

    def LoadFile(self):
        print('LoadFile', self.JsonFile)
        # Note one should always validate that they have a valid file prior to opening it
        # isfile() -- and checking the file extension are two methods I use
        JsonData = open(self.JsonFile[0], "r")
        self.CenterPane.JSonTable = json.load(JsonData)
        print('JSonTable', self.JSonTable)
        self.CenterPane.TreeRoot = self.CenterPane.invisibleRootItem()
        self.CenterPane.fill_item(self.CenterPane.TreeRoot, self.CenterPane.JSonTable)

    def SaveFile(self):
        # Either to a new file or overwriting the exiting file
        # but basically you are now just saving your JsonTable
        # to file -- you could just loop through it manually or
        # I think there are wheels already invented to handle
        # Json objects like this and print them out to a file
        print('Saving Jason File')
        print(self.CenterPane.JSonTable)

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