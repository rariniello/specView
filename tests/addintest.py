import os
import sys
import numpy as np
from addins.addin import Addin

from PyQt5.QtWidgets import QAction

scriptPath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.realpath(os.path.join(scriptPath, '..')))


import numpy as np



name = 'Test-Addin'


def createAddin(interface: object):
    """ Creates and returns an instance of the addin object. 
    
    Args:
        mainWindow: A specView addin interface instance.
    
    Returns:
        addin: The instance of the addin object.
    """
    return AddinTest(interface)


class AddinTest(Addin):
    """ An addin is created when its checkbox is checked in the addin screen. 
    
    It is deleted when the checkbox is unchecked or the item is deleted from the list in the addin screen.
    The addin has a reference to the main window, the addin can interact with th main window using the 
    following interface:
        Modify the plot by directly accessing mainWindow.specPlot or mainWindow.plotDataItem
        Add actions to the main window by adding them to the mainWindow.toolbar
    """
    def __init__(self, specView):
        super().__init__(specView)
        self.actionTest = QAction()
        self.actionTest.setObjectName("actionTest")
        self.actionTest.setText("Test Action")
        self.sv.addAction(self.actionTest)
        self.sv.addSeparator()

        pdi = self.sv.getPlotDataItem()
        pdi.setFillBrush('r')
        pdi.setFillLevel(500)
    

    def processSpectrum(self, lam: np.ndarray, I: np.ndarray) -> np.ndarray:
        """ Modifies the spectrum before displaying it. 

        Args:
            lam: Wavelength of each point in the spectrum [nm].
            I: Intensity at each wavelength in the spectrum [counts].
        """
        return I
    

    def removeAddin(self):
        """ Cleans up after the addin. """
        super().removeAddin()