import os
import sys


specViewPath = None
savePath = None


def defPaths():
    global specViewPath
    global savePath

    specViewPath = getSpecViewPath()


def getSpecViewPath():
    # _MEIPASS is the path to the bundle folder, set by the pyinstaller bootloader
    if hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS
    if isFrozen():
        base = getattr(sys.modules['__main__'], '__file__', sys.executable)
    else:
        base = __file__
    path = os.path.dirname(os.path.realpath(os.path.abspath(base)))
    return path


def isFrozen() -> bool:
    # frozen attribute is added by pyinstaller
    if hasattr(sys, 'frozen'):
        return True
    else:
        return False