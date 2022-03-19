from PyQt5 import QtWidgets, uic
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QSlider, QTextEdit, QFileDialog, QScrollBar, QComboBox, QCheckBox, QScrollBar, QLCDNumber, QLineEdit

import main
import classes
# Initializes all event triggers


def initConnectors(self):

    # Browse button
    self.BrowseButton = self.findChild(QPushButton, "BrowseButton")
    self.BrowseButton.clicked.connect(self.Browse)

    # Export Button
    self.ExportBtn = self.findChild(QPushButton, "ExportBtn")
    self.ExportBtn.clicked.connect(self.ExportPDF)

    # Zoom Buttons
    self.ZoomIn = self.findChild(QPushButton, "ZoomIn")
    self.ZoomIn.clicked.connect(self.ZoomInFunction)

    self.ZoomOut = self.findChild(QPushButton, "ZoomOut")
    self.ZoomOut.clicked.connect(self.ZoomOutFunction)

    self.PausePlayBtn = self.findChild(QPushButton, "PausePlayBtn")
    self.PausePlayBtn.clicked.connect(self.TogglePause)

    # Signal Colour Button
    self.SignalColour = self.findChild(QPushButton, "SignalColour")
    self.SignalColour.clicked.connect(
        lambda: main.MainWindow.SelectSignalColour(self))

    # self.ShowHide = self.findChild(QCheckBox, "ShowHide")
    # self.ShowHide.stateChanged.connect(
    #     lambda: ChannelLineArr[SignalSelectedIndex].UpdateHide())

    self.ThemesMenu = self.findChild(QComboBox, "ThemesMenu")
    self.ThemesMenu.currentIndexChanged.connect(lambda: main.MainWindow.SetSpectroTheme(
        self, self.ThemesMenu.currentText()))  # on index change

    # Updates global variable (SignalSelectedIndex) on combobox change
    self.ChannelsMenu = self.findChild(QComboBox, "ChannelsMenu")
    self.ChannelsMenu.currentIndexChanged.connect(lambda: classes.SetSelectedIndex(
        self.ChannelsMenu.currentIndex(), "Signal"))  # on index change

    # Hide/Unhide checkbox
    self.ShowHide = self.findChild(QCheckBox, "ShowHide")
    self.ShowHide.stateChanged.connect(
        lambda: main.MainWindow.ToggleHide(self, self.ShowHide.isChecked()))

    # Updates SpectroSelectedIndex on change
    self.SpectroMenu = self.findChild(QComboBox, "SpectroMenu")
    self.SpectroMenu.currentIndexChanged.connect(lambda: main.MainWindow.SetSpectroSelectedIndex(self,
                                                                                                 self.SpectroMenu.currentIndex()))

    # Scrollbars

    self.horizontalScrollBar = self.findChild(
        QScrollBar, "horizontalScrollBar")
    self.horizontalScrollBar.valueChanged.connect(
        lambda: self.horizontalScrollBarFunction())

    self.horizontalScrollBar.sliderMoved.connect(
        lambda: self.IsHeldH())

    self.horizontalScrollBar.sliderReleased.connect(
        lambda: self.NotHeldH())

   # vertical

    self.verticalScrollBar = self.findChild(
        QScrollBar, "verticalScrollBar")
    self.verticalScrollBar.valueChanged.connect(
        lambda: self.verticalScrollBarFunction())

    self.verticalScrollBar.sliderMoved.connect(
        lambda: self.IsHeldV())

    self.verticalScrollBar.sliderReleased.connect(
        lambda: self.NotHeldV())
    # Cine speed slider

    self.SpeedSlider = self.findChild(QSlider, "SpeedSlider")
    self.SpeedSlider.valueChanged.connect(
        lambda: self.SpeedSliderFunction(self.SpeedSlider.value()))
    # call UpdateCineSpeed() on change

    # Spectrogram Frequency Range Sliders

    self.SpeedLCD = self.findChild(QLCDNumber, "SpeedLCD")
    self.SpeedSlider.valueChanged.connect(
        lambda: self.SpeedLCD.display(round((self.SpeedSlider.value()/100)*4)/4))

    self.EditLabel = self.findChild(QLineEdit, "EditLabelLine")
    self.EditLabel.returnPressed.connect(
        lambda: self.EditLabelFunction(self.EditLabel.text()))
    self.EditLabel.returnPressed.connect(
        lambda: self.EditLabel.clear())



