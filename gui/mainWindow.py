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
import config

class SpecViewMainWindow(QMainWindow, ui_MainWindow.Ui_MainWindow):
    requestSpectrum = pyqtSignal()
    specClosed = pyqtSignal()
    requestExposureChange = pyqtSignal(float)
    requestAverageShots = pyqtSignal(int)


    def __init__(self, parent=None, icon=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalSlots()
        self.refreshSpecList()
        self.createSpecPlot()
        self.streaming = False
        self.takingBackground = False
        self.background = None
        self.maxCount = 10
        self.count = 0
        self.lastTime = time.time()

        self.backgroundProgressBar.setMaximum(self.backgroundShotsField.value())
    

    def connectSignalSlots(self):
        #self.selectSpecField
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
        #self.backgroundShotsField
        self.takeBackgroundButton.clicked.connect(self.takeBackground)
        self.showBackgroundCheck.stateChanged.connect(self.showBackground)
        self.subtractBackgroundCheck.stateChanged.connect(self.subtractBackground)
        self.averageShotsCheck.stateChanged.connect(self.averageShots)
        #self.averageShotsField


    def createSpecPlot(self):
        plot = self.specPlot
        self.plotDataItem = plot.plot([0], [0])
        self.plotDataItem.setClipToView(True)
        self.plotDataItem.setDownsampling(auto=True, method='peak')
        plot.setLabel('left', "Intensity", units='Counts')
        # TODO fix this unit labelling
        plot.setLabel('bottom', "Wavelength", units='nm', unitPrefix='n')


    def getI(self):
        if self.showBackgroundCheck.isChecked() and self.background is not None:
            I = self.background
        elif self.subtractBackgroundCheck.isChecked() and not self.takingBackground and self.background is not None:
            I = self.I - self.background
        else:
            I = self.I
        return I

    
    def updateSpecPlot(self):
        I = self.getI()
        self.plotDataItem.setData(self.lam, I)


    @pyqtSlot()
    def connectSpec(self):
        self.specClosed.emit()
        spec = self.selectSpecField.currentData()
        self.specName = self.selectSpecField.currentText()
        if self.specName == "":
            return
        
        self.statusbar.showMessage("Connecting to spectrometer...")
        self.thread = QThread()
        self.worker = worker = Worker()
        worker.spec = spec
        worker.moveToThread(self.thread)
        # TODO fix crash when clicking connect and already connected
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.started.connect(self.worker.connectSpec)

        self.specClosed.connect(worker.disconnectSpec)
        self.requestSpectrum.connect(worker.getSpectrum)
        self.requestExposureChange.connect(worker.changeExposure)
        worker.update.connect(self.doUpdate)
        worker.connected.connect(self.onConnect)
        
        self.thread.start()
        self.changeExposure()
        self.startButton.setEnabled(True)
        self.takeBackgroundButton.setEnabled(True)
        self.saveButton.setEnabled(True)
    

    @pyqtSlot(np.ndarray, np.ndarray)
    def doUpdate(self, lam, I):
        self.lam = lam
        self.I = I
        self.updateSpecPlot()
        if self.takingBackground and self.count < self.maxCount:
            if self.background is None:
                self.background = np.zeros(len(self.I))
            self.background += self.I
            self.count += 1
            self.backgroundProgressBar.setValue(self.count)
            self.requestSpectrum.emit()
        elif self.takingBackground and self.count == self.maxCount:
            self.takingBackground = False
            self.background += self.I
            self.background /= self.maxCount
            self.backgroundProgressBar.setValue(self.maxCount)
            self.showBackgroundCheck.setEnabled(True)
            self.subtractBackgroundCheck.setEnabled(True)
            self.pauseButton.setEnabled(False)
            self.startButton.setEnabled(True)
        if self.streaming:
            self.requestSpectrum.emit()
        currentTime = time.time()
        elapsed = currentTime - self.lastTime
        frameRate = 1.0/elapsed
        print(frameRate)
        self.lastTime = currentTime


    @pyqtSlot()
    def refreshSpecList(self):
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
        self.showBackgroundCheck.setChecked(False)
        self.streaming = True
        self.requestSpectrum.emit()
        self.pauseButton.setEnabled(True)


    @pyqtSlot()
    def pause(self):
        self.streaming = False
        self.takingBackground = False
        self.pauseButton.setEnabled(False)
        self.startButton.setEnabled(True)


    @pyqtSlot()
    def save(self):
        I = self.getI()
        filename = QFileDialog.getSaveFileName(self, "Save Spectrum As", config.specViewPath, "Text File (*.txt)")[0]
        N = len(I)
        data = np.zeros((N, 2))
        data[:, 0] = self.lam
        data[:, 1] = I
        np.savetxt(filename, data, header="Wavelength (nm)\tIntensity (counts)")


    @pyqtSlot()
    def exp1(self):
        self.exposureField.setValue(1)
        self.requestExposureChange.emit(1)


    @pyqtSlot()
    def exp2(self):
        self.exposureField.setValue(10)
        self.requestExposureChange.emit(10)


    @pyqtSlot()
    def exp3(self):
        self.exposureField.setValue(100)
        self.requestExposureChange.emit(100)


    @pyqtSlot()
    def exp4(self):
        self.exposureField.setValue(1000)
        self.requestExposureChange.emit(1000)


    @pyqtSlot()
    def takeBackground(self):
        self.backgroundProgressBar.reset()
        self.showBackgroundCheck.setChecked(False)
        self.backgroundProgressBar.setMaximum(self.backgroundShotsField.value())
        self.background = None
        self.streaming = False
        self.takingBackground = True
        self.count = 1
        self.maxCount = self.backgroundShotsField.value()
        self.requestSpectrum.emit()
        self.pauseButton.setEnabled(True)
        self.startButton.setEnabled(False)


    @pyqtSlot()
    def changeExposure(self):
        time = self.exposureField.value()
        self.requestExposureChange.emit(time)


    @pyqtSlot(int)
    def showBackground(self, state):
        self.updateSpecPlot()


    @pyqtSlot(int)
    def subtractBackground(self, state):
        self.updateSpecPlot()


    @pyqtSlot(int)
    def averageShots(self, state):
        pass


    @pyqtSlot()
    def onConnect(self):
        self.statusbar.showMessage("Connected to spectrometer {}".format(self.specName))


    def closeEvent(self, event):
        """ Override the close method to disconnect the spectrometer. """
        self.specClosed.emit()
        event.accept()


class Worker(QObject):
    finished = pyqtSignal()
    update = pyqtSignal(np.ndarray, np.ndarray)
    connected = pyqtSignal()
    connectionFailed = pyqtSignal()
    

    @pyqtSlot()
    def connectSpec(self):
        try:
            self.SP = sb.Spectrometer(self.spec)
        except TypeError:
            self.connectionFailed.emit()
            return
        self.connected.emit()
    

    @pyqtSlot()
    def disconnectSpec(self):
        self.SP.close()
        self.finished.emit()
    

    @pyqtSlot(float)
    def changeExposure(self, value):
        time = value*1e3
        self.SP.integration_time_micros(time)
    

    @pyqtSlot()
    def getSpectrum(self):
        lam, I = self.SP.spectrum(correct_nonlinearity=True)
        self.update.emit(lam, I)
    
