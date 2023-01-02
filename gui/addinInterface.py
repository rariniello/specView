from PyQt5.QtWidgets import QWidget, QAction
import pyqtgraph as pg


class AddinInterface():
    """ Defines the public API addins use to interact with the main window. """
    def __init__(self, mainWindow):
        self.__mainWindow = mainWindow
        self.actions = []
    

    def getPlotDataItem(self) -> pg.PlotDataItem:
        """ Returns the pyqtgraph plotDataItem for the spectrum. """
        return self.__mainWindow.plotDataItem
    

    def getPlotWidget(self) -> pg.PlotWidget:
        """ Returns the pyqtgraph PlotWidget used to display the spectrum. """
        return self.__mainWindow.specPlot
    

    def addAction(self, action: QAction):
        """ Adds the given action to the toolBar. 
        
        Args:
            action: Action to add to the end of the mainWindow toolBar.
        """
        toolBar = self.__mainWindow.toolBar
        toolBar.addAction(action)
        self.actions.append(action)
    

    def addSeparator(self):
        """ Adds a separator to the toolBar. """ 
        toolBar = self.__mainWindow.toolBar
        action = toolBar.addSeparator()
        self.actions.append(action)
    

    def addWidget(self, widget: QWidget):
        """ Adds a widget to the toolBar. 
        
        Args:
            widget: Widget to add to the end of the mainWindow toolBar.
        """ 
        toolBar = self.__mainWindow.toolBar
        action = toolBar.addWidget(widget)
        self.actions.append(action)
    

    def _removeActions(self):
        """ Removes all previously added actions from the toolBar. """
        toolBar = self.__mainWindow.toolBar
        for action in self.actions:
            toolBar.removeAction(action)
    

    def cleanUp(self):
        """ Cleans up changes made to the main window gui. """
        self._removeActions()
            