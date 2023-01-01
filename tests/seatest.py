import os
import sys
import numpy as np
from scipy.signal import savgol_filter
import time

scriptPath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.realpath(os.path.join(scriptPath, '..')))

def list_devices():
    """ Returns a list of SeaBreezeDevices. """
    return [SeaBreezeDevice()]


class SeaBreezeDevice():
    """ Testing class that mimics seabreeze.Spectrometer. 
    
    Only the methods called by SpecView are implemented.
    """
    def __init__(self):
        self.serial_number = '12345678'
        self.model = 'SpecTest'


class Spectrometer():
    def __init__(self, spec):
        self.__multi = 1.0
        filepath = os.path.join("tests", "laserSpectrum.txt")
        data = np.loadtxt(filepath)
        self.lam = data[:, 0]
        self.I = data[:, 1]
        self.I = savgol_filter(self.I, 9, 3)
        self.pixels = len(self.lam)

    
    def integration_time_micros(self, time):
        """ Sets a multiplier that acts like an integration time. """
        self.__multi = time*1e-5


    def spectrum(self, correct_nonlinearity=False):
        """ Returns a tuple containing both wavelengths and intensities of the spectrum. """
        I = self.I * self.__multi
        rng = np.random.default_rng()
        noise = rng.standard_normal(self.pixels)
        I += 20 * noise + 900
        I = I.astype(int)
        sel = I < 0
        I[sel] = 0.0
        sel = I >= 16384
        I[sel] = 16283
        time.sleep(self.__multi*0.1)
        return self.lam, I


    def close(self):
        pass