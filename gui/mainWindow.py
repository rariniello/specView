import os
import numpy as np
import time
import seabreeze.spectrometers as sb

from PyQt5.QtWidgets import (
    QMainWindow, QFileDialog, QAction, QFileDialog
)
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QThread
from PyQt5 import QtCore, QtGui, QtWidgets

import gui.ui.ui_MainWindow as ui_MainWindow
from gui.worker import Worker
import config

class SpecViewMainWindow(QMainWindow, ui_MainWindow.Ui_MainWindow):
    """ Class that handles the main window and the gui functionality.
    
    The spectrometer operates in a different thread from th gui.
    Averaging over multiple shots occurs in the spectrometer thread.
    Background subtraction and everything else occurs in the main gui thread.
    """
    # XXX if th background is shown and save is clicked, does it save the background?
    requestSpectrum = pyqtSignal()
    specClosed = pyqtSignal()
    requestExposureChange = pyqtSignal(float)
    requestAverageShots = pyqtSignal(int)
    requestStopAverage = pyqtSignal()


    def __init__(self, parent=None, icon=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalSlots()
        self.refreshSpecList()
        self.createSpecPlot()
        # Flags for the current state
        self.streaming = False # If the gui is streaming, i.e. requesting the spectrum. False when taking backgrounds
        self.takingBackground = False
        self.streamingBeforeBackground = False # Used to restart streaming automatically after a background is taken
        # Variables used for taking and subtracting backgrounds
        self.background = None
        self.maxCount = 10
        self.count = 0
        self.lastTime = time.time()

        # Steps to initialize the gui
        self.backgroundProgressBar.setMaximum(self.backgroundShotsField.value())
    

    def connectSignalSlots(self):
        """ Connects signals from gui widgets to slots in this class. """
        self.connectButton.clicked.connect(self.connectSpec)
        self.refreshButton.clicked.connect(self.refreshSpecList)
        self.startButton.clicked.connect(self.start)
        self.pauseButton.clicked.connect(self.pause)
        self.saveButton.clicked.connect(self.save)
        self.exposureField.editingFinished.connect(self.changeExposure)
        self.exp1Button.clicked.connect(self.exp1)
        self.exp2Button.clicked.connect(self.exp2)
        self.exp3Button.clicked.connect(self.exp3)
        self.exp4Button.clicked.connect(self.exp4)
        self.takeBackgroundButton.clicked.connect(self.takeBackground)
        self.showBackgroundCheck.stateChanged.connect(self.showBackground)
        self.subtractBackgroundCheck.stateChanged.connect(self.subtractBackground)
        self.averageShotsCheck.stateChanged.connect(self.averageShots)
        self.averageShotsField.editingFinished.connect(self.averageShots)


    def createSpecPlot(self):
        """ Initializes the pyqtgraph plot used to show the spectrum. """
        plot = self.specPlot
        self.plotDataItem = plot.plot([0], [0])
        self.plotDataItem.setClipToView(True)
        self.plotDataItem.setDownsampling(auto=True, method='peak')
        plot.setLabel('left', "Intensity", units='Counts')
        # TODO fix this unit labelling
        plot.setLabel('bottom', "Wavelength", units='nm', unitPrefix='n')


    def getI(self) -> np.ndarray:
        """ Performs pre-processing on the spectrum. 
        
        Performs background subtraction if the subtract background box is checked.
        Called when updating the plot and saving the spectrum.

        Returns:
            I: Array with the processed spectral intensity.
        """
        if self.showBackgroundCheck.isChecked() and self.background is not None:
            I = self.background
        elif self.subtractBackgroundCheck.isChecked() and not self.takingBackground and self.background is not None:
            I = self.I - self.background
        else:
            I = self.I
        return I

    
    def updateSpecPlot(self):
        """ Updates the spectrometer plot. """
        I = self.getI()
        self.plotDataItem.setData(self.lam, I)


    @pyqtSlot()
    def connectSpec(self):
        """ Creates the worker thread for communicating with the spectrometer.
        
        Asks the worker thread to connect to the spectrometer and sets spectrometer settings.
        """
        # Close any already connected spectrometers
        self.specClosed.emit()
        spec = self.selectSpecField.currentData()
        self.specName = self.selectSpecField.currentText()
        if self.specName == "":
            return
        
        self.statusbar.showMessage("Connecting to spectrometer...")
        # Spawn the worker thread
        self.thread = QThread()
        self.worker = Worker(spec)
        self.worker.moveToThread(self.thread)
        # TODO fix crash when clicking connect and already connected
        # Connect signals and slots to control thread startup and shutdown
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.started.connect(self.worker.connectSpec)

        # Connect signals and slots between the worker and the gui
        self.specClosed.connect(self.worker.disconnectSpec)
        self.requestSpectrum.connect(self.worker.getSpectrum)
        self.requestExposureChange.connect(self.worker.changeExposure)
        self.requestAverageShots.connect(self.worker.startAverage)
        self.requestStopAverage.connect(self.worker.stopAverage)
        self.worker.update.connect(self.doUpdate)
        self.worker.connected.connect(self.onConnect)
        
        # Start the thread and set initial spectrometer parameters
        self.thread.start()
        self.changeExposure()
    

    @pyqtSlot(np.ndarray, np.ndarray)
    def doUpdate(self, lam: np.ndarray, I: np.ndarray):
        """ Updates the plot/gui when a new spectrum is recieved. 
        
        Args:
            lam: Array of wavelengths for the spectrum.
            I: Array of intensities for the spectrum.
        """
        self.lam = lam
        self.I = I
        self.updateSpecPlot()
        # When taking backgrounds streaming is false
        if self.takingBackground:
            self.doBackgroundUpdate(lam, I)
        elif self.streaming:
            self.requestSpectrum.emit()
        self.printFramerate()
    

    def printFramerate(self):
        """ Calculates the framerate and prints it to the statusbar. """
        currentTime = time.time()
        elapsed = currentTime - self.lastTime
        if elapsed == 0:
            return
        frameRate = 1.0/elapsed
        self.statusbar.showMessage(self.baseMessage + "Streaming at {:0.2f} fps".format(frameRate))
        self.lastTime = currentTime
    

    def doBackgroundUpdate(self, lam, I):
        """ Updates the plot/gui and background when a new spectrum is recieved while taking background. 
        
        Args:
            lam: Array of wavelengths for the spectrum.
            I: Array of intensities for the spectrum.
        """
        # Still taking the background, update the plot and progress bar
        if self.count < self.maxCount:
            if self.background is None:
                self.background = np.zeros(len(self.I))
            self.background += self.I
            self.count += 1
            self.requestSpectrum.emit()
            self.backgroundProgressBar.setValue(self.count)
        # Done taking the background, update the plot and re-enable gui elements
        elif self.count == self.maxCount:
            self.takingBackground = False
            self.background += self.I
            self.background /= self.maxCount
            if self.streamingBeforeBackground:
                self.streamingBeforeBackground = False
                self.start()
            # Update QUI elements
            self.backgroundProgressBar.setValue(self.maxCount)
            self.showBackgroundCheck.setEnabled(True)
            self.subtractBackgroundCheck.setEnabled(True)
            self.pauseButton.setEnabled(False)
            self.startButton.setEnabled(True)


    @pyqtSlot()
    def refreshSpecList(self):
        """ Detects connected spectrometers and updates the spectrometer field. """
        spectrometers = sb.list_devices()
        self.selectSpecField.clear()
        deviceFound = False
        for spec in spectrometers:
            serial = spec.serial_number
            model = spec.model
            text = model + ': ' + serial
            self.selectSpecField.addItem(text, spec)
            deviceFound = True
        if deviceFound:
            self.connectButton.setEnabled(True)
        else:
            self.connectButton.setEnabled(False)


    @pyqtSlot()
    def start(self):
        """ Starts streaming the spectrum from the spectrometer. """
        self.showBackgroundCheck.setChecked(False)
        self.streaming = True
        self.requestSpectrum.emit()
        self.pauseButton.setEnabled(True)


    @pyqtSlot()
    def pause(self):
        """ Stops streaming the spectrum. """
        self.streaming = False
        self.takingBackground = False
        self.pauseButton.setEnabled(False)
        self.startButton.setEnabled(True)


    @pyqtSlot()
    def save(self):
        """ Saves the spectrum to disk. 
        
        Saves the exact spectrum shown in the plot, i.e., if the background is subtracted
        from the plot it will also be subtracted in the saved file.
        """
        I = self.getI()
        filename = QFileDialog.getSaveFileName(self, "Save Spectrum As", config.specViewPath, "Text File (*.txt)")[0]
        N = len(I)
        data = np.zeros((N, 2))
        data[:, 0] = self.lam
        data[:, 1] = I
        np.savetxt(filename, data, header="Wavelength (nm)\tIntensity (counts)")


    @pyqtSlot()
    def takeBackground(self):
        """ Starts the background saving process. """
        # Update GUI elements
        self.backgroundProgressBar.reset()
        self.showBackgroundCheck.setChecked(False)
        self.backgroundProgressBar.setMaximum(self.backgroundShotsField.value())
        self.pauseButton.setEnabled(True)
        self.startButton.setEnabled(False)
        # Set the appropriate flags and request the spectrum
        if self.streaming:
            self.streamingBeforeBackground = True
        self.background = None
        self.streaming = False
        self.takingBackground = True
        self.count = 1
        self.maxCount = self.backgroundShotsField.value()
        self.requestSpectrum.emit()


    @pyqtSlot()
    def changeExposure(self):
        """ Sets the camera exposure from the exposure field. """
        time = self.exposureField.value()
        self.requestExposureChange.emit(time)
    

    @pyqtSlot()
    def exp1(self):
        """ Sets the camera exposure to 1ms. """
        self.exposureField.setValue(1)
        self.requestExposureChange.emit(1)


    @pyqtSlot()
    def exp2(self):
        """ Sets the camera exposure to 10ms. """
        self.exposureField.setValue(10)
        self.requestExposureChange.emit(10)


    @pyqtSlot()
    def exp3(self):
        """ Sets the camera exposure to 100ms. """
        self.exposureField.setValue(100)
        self.requestExposureChange.emit(100)


    @pyqtSlot()
    def exp4(self):
        """ Sets the camera exposure to 1s. """
        self.exposureField.setValue(1000)
        self.requestExposureChange.emit(1000)


    @pyqtSlot(int)
    def showBackground(self, state):
        """ Shows the current background. """
        self.updateSpecPlot()


    @pyqtSlot(int)
    def subtractBackground(self, state):
        """ Shows the plot with the background subtracted. """
        self.updateSpecPlot()


    @pyqtSlot()
    def averageShots(self):
        """ Tells the spectrometer thread to start averaging over multiple shots. """
        state = self.averageShotsCheck.isChecked()
        if state:
            shots = self.averageShotsField.value()
            self.requestAverageShots.emit(shots)
        if not state:
            self.requestStopAverage.emit()


    @pyqtSlot()
    def onConnect(self):
        """ Updates the gui when the spectrometer is connected. """
        self.statusbar.showMessage("Connected to spectrometer {}".format(self.specName))
        self.baseMessage = "Connected to spectrometer {} | ".format(self.specName)
        self.startButton.setEnabled(True)
        self.takeBackgroundButton.setEnabled(True)
        self.saveButton.setEnabled(True)
        self.connectButton.setEnabled(False)
        self.refreshButton.setEnabled(False)


    def closeEvent(self, event):
        """ Override the close method to disconnect the spectrometer. """
        self.specClosed.emit()
        event.accept()
