import os
import sys
import config
import setup


if __name__ == '__main__':


    config.defPaths()
    # Compile designer files each time we run if we are in a development environment
    if not config.isFrozen():
        setup.build_ui()
    
    # We import in the if statement in case we ever want to check that
    # dependencies exist before we start importing

    from PyQt5.QtWidgets import QApplication
    from PyQt5 import QtCore

    # app and mainWin are defined globably in the application
    # best to avoid defining things here so we don't clutter the global namespace
    app = QApplication(sys.argv)

    # XXX For pyqtgraph, not sure this does anything
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
    QApplication.setHighDpiScaleFactorRoundingPolicy(QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    import pyqtgraph as pg
    # Set pyqtgraph defaults
    pg.setConfigOption('background', 'w')
    pg.setConfigOption('foreground', 'k')
    pg.setConfigOption('antialias', True)


    from gui import mainWindow

    # If we are testing without a spectrometer, monkey patch the seabreeze library
    if False:
        import tests.seatest as sb
        from gui import worker
        mainWindow.sb = sb
        worker.sb = sb
    
    mainWin = mainWindow.SpecViewMainWindow()
    
    mainWin.show()
    sys.exit(app.exec())