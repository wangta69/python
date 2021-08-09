# -*- coding: utf-8 -*-
"""
earlybirdMain.py:
    A wrapper for the EarlybirdTree class (defined in earlybirdTree.py).
    The wrapper allows for simple menu/toolbar-based user interaction
    with an earlybird to do tree. Includes undo/redo functionality.
"""
import sys
import os
from PyQt5 import QtGui, QtCore
from earlybirdTree import EarlybirdTree

class EarlybirdMain(QtGui.QMainWindow):
    '''Main window to wrap an EarlybirdTree'''
    def __init__(self, filename = None):
        QtGui.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.view = EarlybirdTree(self, filename)
        self.model = self.view.model
        self.windowTitleSet()
        self.setCentralWidget(self.view)
        self.createStatusBar()
        self.createActions()
        self.createToolbars()
        self.createMenus()

    def createToolbars(self):
        '''Create toolbars for actions on files and items'''
        self.fileToolbar = self.addToolBar("File actions")
        self.fileToolbar.addAction(self.fileNewAction)
        self.fileToolbar.addAction(self.fileOpenAction)
        self.fileToolbar.addAction(self.fileSaveAction)
        self.fileToolbar.addAction(self.fileSaveAsAction)
        self.itemToolbar = self.addToolBar("Item actions")
        self.itemToolbar.addAction(self.undoAction)
        self.itemToolbar.addAction(self.redoAction)

    def closeEvent(self, event):
        '''If data has been changed, ask user if they want to save it'''
        if not self.view.undoStack.isClean() and self.view.saveCheck():
            self.view.fileSave()
        self.close()

    def createMenus(self):
        '''Create menu for actions on files'''
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.fileOpenAction)
        self.fileMenu.addAction(self.fileNewAction)
        self.fileMenu.addAction(self.fileSaveAction)
        self.fileMenu.addAction(self.fileSaveAsAction)

    def createActions(self):
        '''Create all actions to be used in toolbars/menus: calls createAction()'''
        #File actions
        self.fileNewAction = self.createAction("&New", slot = self.newFile,
                shortcut = QtGui.QKeySequence.New, tip = "New file",
                status = "Create a new file")
        self.fileOpenAction = self.createAction("&Open...", slot = self.fileOpen,
                shortcut = QtGui.QKeySequence.Open, tip = "Open file",
                status = "Open an existing earlybird tree")
        self.fileSaveAction = self.createAction("&Save", slot = self.fileSave,
                shortcut = QtGui.QKeySequence.Save, tip = "Save file",
                status = "Save file")
        self.fileSaveAsAction = self.createAction("Save &As", slot = self.fileSaveAs,
                shortcut = QtGui.QKeySequence.SaveAs, tip = "Save file as", status = "Save file as")
        #Item actions
        self.undoAction = self.createAction("Undo", slot = self.view.undoStack.undo,
               shortcut = QtGui.QKeySequence.Undo, tip = "Undo",
               status = "Undo changes")
        self.redoAction = self.createAction("Redo", slot = self.view.undoStack.redo,
               shortcut = QtGui.QKeySequence.Redo, tip = "Redo",
               status = "Redo changes")

    def createAction(self, text, slot=None, shortcut=None,
                     tip=None, status = None):
        '''Function called to create each individual action'''
        action = QtGui.QAction(text, self)
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
        if status is not None:
            action.setStatusTip(status)
        if slot is not None:
            action.triggered.connect(slot)
        return action

    def createStatusBar(self):
        self.status = self.statusBar()
        self.status.setSizeGripEnabled(False)
        self.status.showMessage("Ready")

    def fileSaveAs(self):
        self.view.saveTodoDataAs()
        self.windowTitleSet()

    def fileSave(self):
        if self.view.filename:
            self.view.saveTodoData()
        else:
            self.view.saveTodoDataAs()
            self.windowTitleSet()

    def fileOpen(self):
        '''Load earlybird file from memory.'''
        if self.view.loadEarlybirdFile():
            self.model = self.view.model
            self.windowTitleSet()
            if self.view.filename:
                filenameNopath = QtCore.QFileInfo(self.view.filename).fileName()
                self.status.showMessage("Opened file: {0}".format(filenameNopath))

    def newFile(self):
        '''Opens new blank earlybird file'''
        self.view.newFile()
        self.windowTitleSet()

    def windowTitleSet(self):
        '''Displays filename as window title, if it exists.'''
        if self.view.filename:
            self.setWindowTitle("Earlybird - {}[*]".format(os.path.basename(self.view.filename)))
        else:
            self.setWindowTitle("Earlybird - <untitled>")


def main():
    ebApp = QtGui.QApplication(sys.argv)
    mainEb = EarlybirdMain(filename = None)#"simpleTodo.eb"
    mainEb.show()
    undoView = QtGui.QUndoView(mainEb.view.undoStack)
    undoView.show()
    sys.exit(ebApp.exec_())


if __name__ == "__main__":
    main()