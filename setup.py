import sys
import os
from PyQt5 import uic
from PyQt5 import pyrcc_main


def map(uiDirName, uiModName):
    return os.path.join('gui', 'ui'), "ui_"+uiModName


def build_ui():
    uic.compileUiDir('designer', map=map)
    resourceFile = os.path.join('resources', 'resources.qrc')
    fileOut = 'resources_rc.py'
    pyrcc_main.processResourceFile([resourceFile], fileOut, False)


if __name__ == '__main__':


    build_ui()
    sys.exit()