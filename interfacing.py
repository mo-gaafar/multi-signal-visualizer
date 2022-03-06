
# THIS FILE CONTAINS FUNCTION DEFENITIONS AND OBJECTS USED IN MAIN
# IT WILL BE SPLIT INTO MORE LOGICAL MODULES IN THE FUTURE

from asyncio.windows_events import NULL
from main import DebugMode, MainWindow
import string
from PyQt5 import QtWidgets, uic
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QSlider, QTextEdit, QFileDialog, QScrollBar, QComboBox, QCheckBox, QScrollBar, QLCDNumber
# from pyparsing import null_debug_action

import csv
import math

#from pyqtgraph import PlotWidget
import pyqtgraph as pg
import sys

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
import scipy.io
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import time

ChannelLineArr = []

# Global Interface Variables
LabelTextBox = "null"
FreqRangeMin = 0
FreqRangeMax = 15


# TODO: add themes here somehow? create theme object or dictionary?
SpectroTheme = 'viridis'


# Should be updated from combobox (on change)
SignalSelectedIndex = 0
SpectroSelectedIndex = 0


def printDebug(Value):  # Enabled when global debug mode is on
    if DebugMode == 1:
        print(Value)


def SetSelectedIndex(Input, Selector):
    if Selector == "Signal":
        global SignalSelectedIndex
        SignalSelectedIndex = Input
        printDebug("Signal dropdown: " + str(SignalSelectedIndex))


class ChannelLine:

    def __init__(self, Label="Unlabeled", LineColour=0xFFFF00,
                 IsHidden=True, Filepath="null", Time=[], Amplitude=[]):
        self.Label = "untitled"
        self.LineColour = 0xffff00
        self.IsHidden = IsHidden
        self.Filepath = "null"
        self.Time = []
        self.Amplitude = []
        self.TimeArrFull = np.array([])
        self.AmplitudeArrFull = np.array([])

    def UpdateColour(self):
        # self.LineColour =
        # self.LineColour = "NONE"
        # print(self.LineColour)
        PrevColour = self.LineColour
        self.LineColour = MainWindow.SelectSignalColour(self)
        # Keeps previous colour if user cancels/selects black
        if (self.LineColour == "#000000"):
            self.LineColour = PrevColour

        printDebug(str(self.LineColour) +
                   " set as colour for channel: " + str(SignalSelectedIndex))

    # LineColour Getter
    def GetColour(self):
        return self.LineColour

    def UpdateHide(self):
        printDebug("Updated IsHidden")


def initArrays(self):
    for Index in range(3):
        ChannelLineArr.append(ChannelLine())
        print(ChannelLineArr[Index])
    # Global plot channel object that contains related attributes


# TO BE INITIALIZED AS GLOBAL VAR
class PlotterWindow:
    def __init__(self, YAxisRange=(0, 1), XAxisRange=(-1, 1), CineSpeed=1.0):
        self.YAxisRange = YAxisRange  # Tuple containing min/max ranges
        self.XAxisRange = XAxisRange

        self.CineSpeed = 50

    def UpdateCineSpeed(self, Input):
            self.CineSpeed = (50) / (Input/100)
        #MainWindow.timer = QtCore.QTimer()
        #MainWindow.timer.setInterval(100*self.CineSpeed)


class ChannelSpectrogram:
    def __init__(self, FreqRangeMax=1000, FreqRangeMin=0, SelectedChannel=1, SelectedTheme="Default"):
        self.FreqRangeMax = FreqRangeMax
        self.FreqRangeMin = FreqRangeMin
        self.SelectedTheme = SelectedTheme

    def UpdateFreqRange(Input, MinOrMax):
        if MinOrMax == "Min":
            printDebug("Brengan")
        # Updates the object variable
        # Update the attribute in the actual plot
        if MinOrMax == "Max":
            printDebug("Brengan")
        # Updates the object variable
        # Update the attribute in the actual plot

    def UpdateSelectedTheme(ThemeIndex):
        printDebug("Brengan")
        # Updates the object variable
        # Update the attribute in the actual plot


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
        lambda: ChannelLineArr[SignalSelectedIndex].UpdateColour())

    self.ShowHide = self.findChild(QCheckBox, "ShowHide")
    self.ShowHide.stateChanged.connect(
        lambda: ChannelLineArr[SignalSelectedIndex].UpdateHide())

    self.ThemesMenu = self.findChild(QComboBox, "ThemesMenu")
    self.ThemesMenu.currentIndexChanged.connect(lambda: MainWindow.SetSpectroTheme(self, self.ThemesMenu.currentText()))  # on index change

    # Updates global variable (SignalSelectedIndex) on combobox change
    self.ChannelsMenu = self.findChild(QComboBox, "ChannelsMenu")
    self.ChannelsMenu.currentIndexChanged.connect(lambda: SetSelectedIndex(
        self.ChannelsMenu.currentIndex(), "Signal"))  # on index change

    # Updates SpectroSelectedIndex on change
    self.SpectroMenu = self.findChild(QComboBox, "SpectroMenu")
    self.SpectroMenu.currentIndexChanged.connect(lambda: MainWindow.SetSpectroSelectedIndex(self, 
        self.SpectroMenu.currentIndex()))

    # Scrollbars

    self.horizontalScrollBar = self.findChild(
        QScrollBar, "horizontalScrollBar")
    self.horizontalScrollBar.valueChanged.connect(
        lambda: self.horizontalScrollBarFunction(self.horizontalScrollBar.value()))

    self.verticalScrollBar = self.findChild(QScrollBar, "verticalScrollBar")
    self.verticalScrollBar.valueChanged.connect(
        lambda: self.verticalScrollBarFunction(self.verticalScrollBar.value()))

    # Cine speed slider

    self.SpeedSlider = self.findChild(QSlider, "SpeedSlider")
    self.SpeedSlider.valueChanged.connect(
        lambda: self.SpeedSliderFunction(self.SpeedSlider.value()))
    # call UpdateCineSpeed() on change

    # Spectrogram Frequency Range Sliders
    self.MinRangeSlider = self.findChild(QSlider, "MinRangeSlider")
    self.MinRangeSlider.sliderReleased.connect(
        lambda: self.SpectrogramFrequency(self.MinRangeSlider.value(), "min"))

    self.MaxRangeSlider = self.findChild(QSlider, "MaxRangeSlider")
    self.MaxRangeSlider.sliderReleased.connect(
        lambda: self.SpectrogramFrequency(self.MaxRangeSlider.value(), "max"))

    self.SpeedLCD = self.findChild(QLCDNumber, "SpeedLCD")
    self.SpeedSlider.valueChanged.connect(
        lambda: self.SpeedLCD.display(round((self.SpeedSlider.value()/100)*4)/4))

    self.MinLCD = self.findChild(QLCDNumber, "MinLCD")
    self.MinRangeSlider.valueChanged.connect(
        lambda: self.MinLCD.display(self.MinRangeSlider.value()))

    self.MaxLCD = self.findChild(QLCDNumber, "MaxLCD")
    self.MaxRangeSlider.valueChanged.connect(
        lambda: self.MaxLCD.display(self.MaxRangeSlider.value()))
