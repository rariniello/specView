import os
import numpy as np
import time
import json
import seabreeze.spectrometers as sb
from importlib.machinery import SourceFileLoader

from PyQt5.QtWidgets import QDialog, QAbstractItemView, QFileDialog, QListWidgetItem, QMessageBox
from PyQt5.QtCore import pyqtSlot, Qt

import gui.ui.ui_AddinsWindow as ui_AddinsWindow
from gui.addinInterface import AddinInterface
import config


class AddinListItem(QListWidgetItem):
    def __init__(self, name: str, script: object, path: str):
        """ Initializes the list item.
        
        Args:
            name: The name of the addin to display in the list, must be unique.
            script: The script object for the addin (python module).
            path: The full file path to the addin script.
        """
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


class AddinsWindow(QDialog, ui_AddinsWindow.Ui_AddinsWindow):
    """ Class that handles the addins window. """
    addinsSave = 'data/addinsList.json'


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
    

    @pyqtSlot()
    def addAddin(self, filename: str=None):
        """ Opens a file explorer to find the addin python script. """
        if filename is None:
            filename = QFileDialog.getOpenFileName(self, "Load Add-in Script", config.specViewPath, "Python Script (*.py)")[0]
        if filename == '':
            return
        script = SourceFileLoader("addin", filename).load_module()
        name = script.name
        items = self.addinsList.findItems(name, Qt.MatchExactly)
        # Check if an addin with the same name already exists
        if len(items) != 0:
            messageBox = QMessageBox()
            messageBox.warning(self, "Error: Add-in already exists", "The add-in was not loaded because an add-in with the name '{}' already exists.".format(name))
            messageBox.setFixedSize(500,200)
            return
        item = AddinListItem(name, script, filename)
        self.addinsList.addItem(item)
        self.saveCurrentAddins()
    

    @pyqtSlot(QListWidgetItem)
    def listItemChanged(self, addinItem):
        """ Initializes or deinitializes the given addin based on its checkmark status.
        
        If unchecked, the addin object is removed. This allows unchecking/checking to restart the addin.
        """
        if addinItem.checkState() == Qt.Checked:
            script = addinItem.script
            interface = AddinInterface(self.parent)
            try:
                addinItem.addin = script.createAddin(interface)
            except AttributeError as err:
                print(err)
                messageBox = QMessageBox()
                messageBox.warning(self, "Error: Add-in initialization failed", "Initializizing the '{}' add-in failed with an attribute error. Check that the addin script has a createAddin function.".format(script.name))
                messageBox.setFixedSize(500,200)
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
            if addinItem.checkState() == Qt.Checked:
                self.cleanupAddin(addinItem, )
            row = self.addinsList.row(addinItem)
            self.addinsList.takeItem(row)
            del addinItem
        self.saveCurrentAddins()
    

    def cleanupAddin(self, addinItem: AddinListItem):
        """ Calls the addins clean up method and deletes references to the addin. """
        addinItem.addin.removeAddin()
        del addinItem.addin


    def loadPreviousAddins(self):
        """ Loads the saved list of addins from disk. If the scripts don't exist, they are ignored. """
        saveName = os.path.abspath(self.addinsSave)
        if not os.path.exists(saveName):
            return False

        with open(saveName, 'r') as f:
            addinFilenames = json.load(f)
        
        for filename in addinFilenames:
            self.addAddin(filename)
    

    def saveCurrentAddins(self):
        """ Saves the current list of addins to disk. """
        N = self.addinsList.count()
        addinFilenames = []
        for i in range(N):
            item = self.addinsList.item(i)
            addinFilenames.append(item.path)

        saveName = os.path.abspath(self.addinsSave)
        if not os.path.exists(os.path.dirname(saveName)):
            return False
        
        with open(saveName, 'w') as f:
            json.dump(addinFilenames, f)
