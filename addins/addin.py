""" Template for an addin script.

The addin script must define:
    name: string that uniquely identifies the addin.
    createAddin: constructor function that return the addin object.
"""
import numpy as np


name = 'Addin'


def createAddin(interface: object):
    """ Creates and returns an instance of the addin object. 
    
    Args:
        mainWindow: A specView addin interface instance.
    
    Returns:
        addin: The instance of the addin object.
    """
    return Addin(interface)


class Addin():
    """ An addin is created when its checkbox is checked in the addin screen. 
    
    It is deleted when the checkbox is unchecked or the item is deleted from the list in the addin screen.
    The addin has a reference to the main window, the addin can interact with th main window using the 
    following interface:
        Modify the plot by directly accessing mainWindow.specPlot or mainWindow.plotDataItem
        Add actions to the main window by adding them to the mainWindow.toolbar
    """
    def __init__(self, specView):
        self.sv = specView
    

    def processSpectrum(self, lam: np.ndarray, I: np.ndarray) -> np.ndarray:
        """ Modifies the spectrum before displaying it. 

        The spectral intensity is passed to this function after averaging and background subtraction.
        Overwrite to modify the spectrum before it is displayed in SpecView window.
        
        Args:
            lam: Wavelength of each point in the spectrum [nm].
            I: Intensity at each wavelength in the spectrum [counts].
        """
        return I
    

    def removeAddin(self):
        """ Cleans up after the addin.
        
        Should clean up the following:
            Remove any modifications done to mainWindow.specPlot or mainWindow.plotDataItem.
            Close any gui windows opened by the addin.
        """
        self.sv.cleanUp()