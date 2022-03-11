
# THIS FILE CONTAINS FUNCTION DEFENITIONS AND OBJECTS USED IN MAIN
# IT WILL BE SPLIT INTO MORE LOGICAL MODULES IN THE FUTURE

from asyncio.windows_events import NULL
from main import DebugMode, MainWindow
import string
from PyQt5 import QtWidgets, uic
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QSlider, QTextEdit, QFileDialog, QScrollBar, QComboBox, QCheckBox, QScrollBar, QLCDNumber, QLineEdit

import pyqtgraph as pg
from pyqtgraph import PlotWidget
import sys

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
import scipy.io
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import utility as util


# Global Interface Variables
LabelTextBox = "null"
FreqRangeMin = 0
FreqRangeMax = 250


# TODO: add themes here somehow? create theme object or dictionary?
SpectroTheme = 'viridis'


# Should be updated from combobox (on change)
SignalSelectedIndex = 0
SpectroSelectedIndex = 0


def SetSelectedIndex(Input, Selector):
    if Selector == "Signal":
        global SignalSelectedIndex
        SignalSelectedIndex = Input
        print(SignalSelectedIndex)
        util.printDebug("Signal dropdown: " + str(SignalSelectedIndex))


class ChannelLine():

    def __init__(self, Label="Unlabeled", LineColour=0xFFFF00, IsHidden=False, Filepath="null", Time=[], Amplitude=[]):
        self.Label = "untitled"
        self.LineColour = 0xffff00
        self.IsHidden = IsHidden
        self.Filepath = "null"
        self.Time = []
        self.Amplitude = []
        self.TimeArrFull = np.array([])
        self.AmplitudeArrFull = np.array([])
        self.PlotWidgetReference = PlotWidget()

    def UpdateColour(self, InputColour):
        PrevColour = self.LineColour
        # Keeps previous colour if user cancels/selects black
        if (InputColour == "#000000"):
            self.LineColour = PrevColour
        else:
            self.LineColour = InputColour

        util.printDebug(str(self.LineColour) +
                        " set as colour for channel: " + str(SignalSelectedIndex))

    # LineColour Getter
    def GetColour(self):
        return self.LineColour

    def UpdateHide(self):
        util.printDebug("Updated IsHidden")

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
        # MainWindow.timer.setInterval(100*self.CineSpeed)


class ChannelSpectrogram:
    def __init__(self, FreqRangeMax=1000, FreqRangeMin=0, SelectedChannel=1, SelectedTheme="Default"):
        self.FreqRangeMax = FreqRangeMax
        self.FreqRangeMin = FreqRangeMin
        self.SelectedTheme = SelectedTheme

    def UpdateFreqRange(Input, MinOrMax):
        if MinOrMax == "Min":
            util.printDebug("Brengan")
        # Updates the object variable
        # Update the attribute in the actual plot
        if MinOrMax == "Max":
            util.printDebug("Brengan")
        # Updates the object variable
        # Update the attribute in the actual plot

    def UpdateSelectedTheme(ThemeIndex):
        util.printDebug("Brengan")
        # Updates the object variable
        # Update the attribute in the actual plot


def initSpectroRangeSliders(self):
    self.MinRangeSlider = self.findChild(QSlider, "MinRangeSlider")
    self.MinRangeSlider.setMaximum(FreqRangeMax)
    self.MinRangeSlider.setValue(0)
    self.MinRangeSlider.sliderReleased.connect(
        lambda: self.SpectrogramFrequency(self.MinRangeSlider.value(), "min"))

    self.MaxRangeSlider = self.findChild(QSlider, "MaxRangeSlider")
    self.MaxRangeSlider.setMaximum(FreqRangeMax)
    self.MaxRangeSlider.setValue(FreqRangeMax)
    self.MaxRangeSlider.sliderReleased.connect(
        lambda: self.SpectrogramFrequency(self.MaxRangeSlider.value(), "max"))

    self.MinLCD = self.findChild(QLCDNumber, "MinLCD")
    self.MinLCD.display(FreqRangeMin)
    self.MinRangeSlider.valueChanged.connect(
        lambda: self.MinLCD.display(self.MinRangeSlider.value()))

    self.MaxLCD = self.findChild(QLCDNumber, "MaxLCD")
    self.MaxLCD.display(FreqRangeMax)
    self.MaxRangeSlider.valueChanged.connect(
        lambda: self.MaxLCD.display(self.MaxRangeSlider.value()))
