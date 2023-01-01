import os
import numpy as np
import time
import seabreeze.spectrometers as sb
from importlib.machinery import SourceFileLoader

from PyQt5.QtWidgets import (
    QDialog, QAbstractItemView, QFileDialog, QListWidgetItem
)
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QThread, Qt
from PyQt5 import QtCore, QtGui, QtWidgets

import gui.ui.ui_AddinsWindow as ui_AddinsWindow
import config


class AddinsWindow(QDialog, ui_AddinsWindow.Ui_AddinsWindow):
    """ Class that handles the addins window. """


    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalSlots()
        self.addinsList.setDragDropMode(QAbstractItemView.InternalMove)
        self.loadPreviousAddins()
        self.parent = parent

        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
    

    def connectSignalSlots(self):
        """ Connects signals from gui widgets to slots in this class. """
        self.addButton.clicked.connect(self.addAddin)
        self.okButton.clicked.connect(self.doOk)
        self.deleteButton.clicked.connect(self.deleteAddin)
        self.addinsList.itemChanged.connect(self.listItemChanged)
    

    def addAddin(self):
        """ Opens a file explorer to find the addin python script. """
        filename = QFileDialog.getOpenFileName(self, "Load Add-in Script", config.specViewPath, "Python Script (*.py)")[0]
        if filename == '':
            return
        script = SourceFileLoader("addin", filename).load_module()
        name = script.name
        items = self.addinsList.findItems(name, Qt.MatchExactly)
        # Check if an addin with the same name already exists
        if len(items) != 0:
            # TODO, print a message or something letting the user know the addin already exists
            # Best to do this by emitting a signal and letting the main window deal with it
            return
        item = AddinListItem(name, script, filename)
        self.addinsList.addItem(item)
    

    @pyqtSlot(QListWidgetItem)
    def listItemChanged(self, addinItem):
        """ Initializes or deinitializes the given addin based on its checkmark status.
        
        If unchecked, the addin object is removed. This allows unchecking/checking to restart the addin.
        """
        if addinItem.checkState() == Qt.Checked:
            script = addinItem.script
            try:
                addinItem.addin = script.createAddin(self.parent)
            except AttributeError:
                # TODO make the error warn the user in some way
                print('Error!')
                addinItem.setCheckState(Qt.Unchecked)
        elif addinItem.checkState() == Qt.Unchecked:
            self.cleanupAddin(addinItem)


    def getActiveAddins(self) -> list:
        """ Loads the active addins from the addins window. 
        
        Returns:
            ActieAddins: Currently active addin objects.
        """
        activeAddins = []
        for i in range(self.addinsList.count()):
            addinItem = self.addinsList.item(i)
            if addinItem.checkState() == Qt.Checked:
                activeAddins.append(addinItem.addin)
        return activeAddins


    def doOk(self):
        """ Hides the window and emits a signal that new addins have been selected. """
        self.hide()
    

    def deleteAddin(self):
        """ Removes the selected addins from the list. """
        addinItems = self.addinsList.selectedItems()
        for addinItem in addinItems:
            self.cleanupAddin(addinItem)
            row = self.addinsList.row(addinItem)
            self.addinsList.takeItem(row)
            del addinItem
    

    def cleanupAddin(self, addinItem):
        """ Calls the addins clean up method and deletes references to the addin. """
        addinItem.addin.removeAddin()
        del addinItem.addin


    def loadPreviousAddins(self):
        """ Loads the saved list of addins from disk. If the scripts don't exist, they are ignored. """
        # XXX implement this using a yml file that stores the addin names and filepaths
    

    def saveCurrentAddins(self):
        """ Saves the current list of addins to disk. """
        # XXX implement this using a yml file that stores the addin names and filepaths


class AddinListItem(QListWidgetItem):
    def __init__(self, name, script, path):
        super().__init__(name)
        self.__script = script
        self.__addin = None
        self.path = path
        self.setFlags(self.flags() | Qt.ItemIsUserCheckable)
        self.setCheckState(Qt.Unchecked)


    @property
    def script(self) -> object:
        """ Returns the module object for the script. """
        return self.__script
    

    @property
    def addin(self) -> object:
        """ Returns the addin object if it has been created, otherwise returns None. """
        return self.__addin
    

    @addin.setter
    def addin(self, object: object):
        """ Sets the addin property to the given object. """
        self.__addin = object
    

    @addin.deleter
    def addin(self):
        """ Sets the addin property to None. """
        self.__addin = None
