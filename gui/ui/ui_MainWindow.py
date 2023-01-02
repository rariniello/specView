# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer\MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SpecView(object):
    def setupUi(self, SpecView):
        SpecView.setObjectName("SpecView")
        SpecView.resize(1920, 650)
        SpecView.setBaseSize(QtCore.QSize(100, 0))
        SpecView.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/color.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        SpecView.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(SpecView)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setContentsMargins(4, 4, 4, 4)
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setBaseSize(QtCore.QSize(0, 0))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setContentsMargins(4, 4, 4, 4)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout.setObjectName("gridLayout")
        self.averageKLabel = QtWidgets.QLabel(self.frame)
        self.averageKLabel.setObjectName("averageKLabel")
        self.gridLayout.addWidget(self.averageKLabel, 18, 0, 1, 4)
        self.takeBackgroundButton = QtWidgets.QPushButton(self.frame)
        self.takeBackgroundButton.setEnabled(False)
        self.takeBackgroundButton.setObjectName("takeBackgroundButton")
        self.gridLayout.addWidget(self.takeBackgroundButton, 12, 0, 1, 4)
        self.exp4Button = QtWidgets.QToolButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exp4Button.sizePolicy().hasHeightForWidth())
        self.exp4Button.setSizePolicy(sizePolicy)
        self.exp4Button.setObjectName("exp4Button")
        self.gridLayout.addWidget(self.exp4Button, 7, 3, 1, 1)
        self.backgroundLabel = QtWidgets.QLabel(self.frame)
        self.backgroundLabel.setObjectName("backgroundLabel")
        self.gridLayout.addWidget(self.backgroundLabel, 10, 0, 1, 4)
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 4)
        self.subtractBackgroundCheck = QtWidgets.QCheckBox(self.frame)
        self.subtractBackgroundCheck.setEnabled(False)
        self.subtractBackgroundCheck.setObjectName("subtractBackgroundCheck")
        self.gridLayout.addWidget(self.subtractBackgroundCheck, 15, 0, 1, 4)
        self.averageShotsField = QtWidgets.QSpinBox(self.frame)
        self.averageShotsField.setEnabled(True)
        self.averageShotsField.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.averageShotsField.setMaximum(1000)
        self.averageShotsField.setProperty("value", 10)
        self.averageShotsField.setObjectName("averageShotsField")
        self.gridLayout.addWidget(self.averageShotsField, 19, 1, 1, 2)
        self.backgroundShotsField = QtWidgets.QSpinBox(self.frame)
        self.backgroundShotsField.setEnabled(True)
        self.backgroundShotsField.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.backgroundShotsField.setMaximum(1000)
        self.backgroundShotsField.setProperty("value", 10)
        self.backgroundShotsField.setObjectName("backgroundShotsField")
        self.gridLayout.addWidget(self.backgroundShotsField, 11, 1, 1, 2)
        self.showBackgroundCheck = QtWidgets.QCheckBox(self.frame)
        self.showBackgroundCheck.setEnabled(False)
        self.showBackgroundCheck.setObjectName("showBackgroundCheck")
        self.gridLayout.addWidget(self.showBackgroundCheck, 14, 0, 1, 4)
        self.saveButton = QtWidgets.QToolButton(self.frame)
        self.saveButton.setEnabled(False)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/disk.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.saveButton.setIcon(icon1)
        self.saveButton.setObjectName("saveButton")
        self.gridLayout.addWidget(self.saveButton, 4, 2, 1, 1)
        self.exposureField = QtWidgets.QDoubleSpinBox(self.frame)
        self.exposureField.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.exposureField.setMaximum(10000.0)
        self.exposureField.setProperty("value", 100.0)
        self.exposureField.setObjectName("exposureField")
        self.gridLayout.addWidget(self.exposureField, 6, 0, 1, 3)
        self.line = QtWidgets.QFrame(self.frame)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 9, 0, 1, 4)
        self.line_2 = QtWidgets.QFrame(self.frame)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout.addWidget(self.line_2, 16, 0, 1, 4)
        self.averageShotsCheck = QtWidgets.QCheckBox(self.frame)
        self.averageShotsCheck.setEnabled(True)
        self.averageShotsCheck.setObjectName("averageShotsCheck")
        self.gridLayout.addWidget(self.averageShotsCheck, 17, 0, 1, 4)
        self.exp1Button = QtWidgets.QToolButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exp1Button.sizePolicy().hasHeightForWidth())
        self.exp1Button.setSizePolicy(sizePolicy)
        self.exp1Button.setObjectName("exp1Button")
        self.gridLayout.addWidget(self.exp1Button, 7, 0, 1, 1)
        self.backgroundProgressBar = QtWidgets.QProgressBar(self.frame)
        self.backgroundProgressBar.setMaximum(10)
        self.backgroundProgressBar.setProperty("value", 0)
        self.backgroundProgressBar.setTextVisible(True)
        self.backgroundProgressBar.setInvertedAppearance(False)
        self.backgroundProgressBar.setObjectName("backgroundProgressBar")
        self.gridLayout.addWidget(self.backgroundProgressBar, 13, 0, 1, 4)
        self.exp2Button = QtWidgets.QToolButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exp2Button.sizePolicy().hasHeightForWidth())
        self.exp2Button.setSizePolicy(sizePolicy)
        self.exp2Button.setObjectName("exp2Button")
        self.gridLayout.addWidget(self.exp2Button, 7, 1, 1, 1)
        self.startButton = QtWidgets.QToolButton(self.frame)
        self.startButton.setEnabled(False)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/icons/control.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.startButton.setIcon(icon2)
        self.startButton.setObjectName("startButton")
        self.gridLayout.addWidget(self.startButton, 4, 0, 1, 1)
        self.selectSpecField = QtWidgets.QComboBox(self.frame)
        self.selectSpecField.setObjectName("selectSpecField")
        self.gridLayout.addWidget(self.selectSpecField, 1, 0, 1, 4)
        self.line_3 = QtWidgets.QFrame(self.frame)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.gridLayout.addWidget(self.line_3, 3, 0, 1, 4)
        self.exposureLabel = QtWidgets.QLabel(self.frame)
        self.exposureLabel.setObjectName("exposureLabel")
        self.gridLayout.addWidget(self.exposureLabel, 5, 0, 1, 4)
        self.exp3Button = QtWidgets.QToolButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exp3Button.sizePolicy().hasHeightForWidth())
        self.exp3Button.setSizePolicy(sizePolicy)
        self.exp3Button.setObjectName("exp3Button")
        self.gridLayout.addWidget(self.exp3Button, 7, 2, 1, 1)
        self.pauseButton = QtWidgets.QToolButton(self.frame)
        self.pauseButton.setEnabled(False)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/icons/control-pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pauseButton.setIcon(icon3)
        self.pauseButton.setObjectName("pauseButton")
        self.gridLayout.addWidget(self.pauseButton, 4, 1, 1, 1)
        self.refreshButton = QtWidgets.QToolButton(self.frame)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/icons/arrow-circle-double-135.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.refreshButton.setIcon(icon4)
        self.refreshButton.setObjectName("refreshButton")
        self.gridLayout.addWidget(self.refreshButton, 2, 3, 1, 1)
        self.connectButton = QtWidgets.QPushButton(self.frame)
        self.connectButton.setEnabled(False)
        self.connectButton.setObjectName("connectButton")
        self.gridLayout.addWidget(self.connectButton, 2, 0, 1, 3)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 1, 0, 1, 1)
        self.horizontalLayout.addWidget(self.frame)
        self.specPlot = PlotWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.specPlot.sizePolicy().hasHeightForWidth())
        self.specPlot.setSizePolicy(sizePolicy)
        self.specPlot.setMinimumSize(QtCore.QSize(0, 0))
        self.specPlot.setObjectName("specPlot")
        self.horizontalLayout.addWidget(self.specPlot)
        SpecView.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(SpecView)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1920, 26))
        self.menubar.setObjectName("menubar")
        SpecView.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(SpecView)
        self.statusbar.setObjectName("statusbar")
        SpecView.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(SpecView)
        self.toolBar.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.toolBar.setMovable(False)
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toolBar.setFloatable(False)
        self.toolBar.setObjectName("toolBar")
        SpecView.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionSettings = QtWidgets.QAction(SpecView)
        self.actionSettings.setEnabled(False)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icons/icons/gear.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSettings.setIcon(icon5)
        self.actionSettings.setObjectName("actionSettings")
        self.actionAddins = QtWidgets.QAction(SpecView)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/icons/icons/application-plus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAddins.setIcon(icon6)
        self.actionAddins.setObjectName("actionAddins")
        self.toolBar.addAction(self.actionSettings)
        self.toolBar.addAction(self.actionAddins)
        self.toolBar.addSeparator()

        self.retranslateUi(SpecView)
        QtCore.QMetaObject.connectSlotsByName(SpecView)

    def retranslateUi(self, SpecView):
        _translate = QtCore.QCoreApplication.translate
        SpecView.setWindowTitle(_translate("SpecView", "SpecView"))
        self.averageKLabel.setText(_translate("SpecView", "Shots to Average"))
        self.takeBackgroundButton.setText(_translate("SpecView", "Take Background"))
        self.exp4Button.setText(_translate("SpecView", "1000"))
        self.backgroundLabel.setText(_translate("SpecView", "Background Shots"))
        self.label.setText(_translate("SpecView", "Select Spectrometer"))
        self.subtractBackgroundCheck.setText(_translate("SpecView", "Subtract Background"))
        self.showBackgroundCheck.setText(_translate("SpecView", "Show Background"))
        self.saveButton.setText(_translate("SpecView", "..."))
        self.averageShotsCheck.setText(_translate("SpecView", "Average Shots"))
        self.exp1Button.setText(_translate("SpecView", "1"))
        self.exp2Button.setText(_translate("SpecView", "10"))
        self.startButton.setText(_translate("SpecView", "..."))
        self.exposureLabel.setText(_translate("SpecView", "Exposure Time (ms)"))
        self.exp3Button.setText(_translate("SpecView", "100"))
        self.pauseButton.setText(_translate("SpecView", "..."))
        self.refreshButton.setText(_translate("SpecView", "..."))
        self.connectButton.setText(_translate("SpecView", "Connect"))
        self.actionSettings.setText(_translate("SpecView", "Settings"))
        self.actionAddins.setText(_translate("SpecView", "Add-ins"))
        self.actionAddins.setToolTip(_translate("SpecView", "ManageAdd-ins"))
from pyqtgraph import PlotWidget
import resources_rc
