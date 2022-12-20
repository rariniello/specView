import os
import numpy as np
import seabreeze.spectrometers as sb

from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QThread


class Worker(QObject):
    finished = pyqtSignal()
    update = pyqtSignal(np.ndarray, np.ndarray)
    connected = pyqtSignal()
    connectionFailed = pyqtSignal()


    def __init__(self, spec):
        super().__init__()
        self.averaging = False
        self.averageArray = None
        self.index = 0
        self.averageShots = 0
        self.spec = spec
    

    @pyqtSlot()
    def connectSpec(self):
        """ Attempts to connect to the sectrometer. """
        try:
            self.SP = sb.Spectrometer(self.spec)
        except TypeError:
            self.connectionFailed.emit()
            return
        self.connected.emit()
    

    @pyqtSlot()
    def disconnectSpec(self):
        """ Closes the connection to the spectrometer. """
        self.SP.close()
        self.finished.emit()
    

    @pyqtSlot(float)
    def changeExposure(self, value: float):
        """ Changes the spectrometers exposure time to the given exposure. 
        
        Args:
            value: Expsorue to set [ms].
        """
        time = value*1e3
        self.SP.integration_time_micros(time)
    

    @pyqtSlot()
    def getSpectrum(self):
        """ Retrieve the spectrum from the device, rolling averages multiple shots if enabled. """
        lam, I = self.SP.spectrum(correct_nonlinearity=True)
        if self.averaging:
            self.averageArray[self.index] = I
            self.index = (self.index + 1) % self.averageShots
            I = np.average(self.averageArray, axis=0)
        self.update.emit(lam, I)

    
    @pyqtSlot(int)
    def startAverage(self, shots: int):
        """ Sets this worker to return the spectrum as a rolling average over the given number of shots.
        
        Args:
            shots: Number of shots to averae over.
        """
        N = self.SP.pixels
        self.averageArray = np.zeros((shots, N))
        self.averageShots = shots
        self.index = 0
        self.averaging = True

    
    @pyqtSlot()
    def stopAverage(self):
        """ Stops this worker from doing a rolling average. """
        self.averaging = False
