import string
from PyQt5 import QtWidgets, uic
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTextEdit, QFileDialog, QScrollBar, QComboBox
#from pyparsing import null_debug_action

from pyqtgraph import PlotWidget
import pyqtgraph as pg
import sys

from main import DebugMode, MainWindow

# Global Interface Variables
LabelTextBox = "null"

# TODO: add themes here somehow? create theme object or dictionary?
SpectroThemesArray = []

CineSpeed = 1  # from 0.1 to 10x

# Should be updated from combobox (on change)
SignalSelectedIndex = 0
SpectroSelectedIndex = 0


def SetSignalIndex(Input):
    global SignalSelectedIndex
    SignalSelectedIndex = Input
    if DebugMode == True:
        print(SignalSelectedIndex)


ChannelLineArr = []


class ChannelLine:

    def __init__(self, Label="Unlabeled", LineColour=0xFFFF00, IsHidden=True, Filename="null"):
        self.Label = Label
        self.LineColour = LineColour
        self.IsHidden = IsHidden
        #self.Filename = Filename

    def UpdateColour(self):
        # self.LineColour =
        #self.LineColour = "NONE"
        # print(self.LineColour)
        PrevColour = self.LineColour
        self.LineColour = MainWindow.SelectSignalColour(self)
        if (self.LineColour == "#000000"):                      # Keeps previous colour if user cancels/selects black
            self.LineColour = PrevColour

        if DebugMode == True:
            print(str(self.LineColour) + " set as colour for channel: " +
                  str(SignalSelectedIndex))

    # LineColour Getter
    def GetColour(self):
        return self.LineColour


def initArrays(self):
    for Index in range(3):
        ChannelLineArr.append(ChannelLine())
        print(ChannelLineArr[Index])
    # Global plot channel object that contains related attributes


def printbtengan():
    print("brengan")


class ChannelSpectrogram:
    def __init__(self, FreqRangeMax=1000, FreqRangeMin=0, SelectedChannel=1, SelectedTheme="Default"):
        self.FreqRangeMax = FreqRangeMax
        self.FreqRangeMin = FreqRangeMin
        self.SelectedTheme = SelectedTheme

    def UpdateFreqRange(Input, MinOrMax):
        if MinOrMax == "Min":
            if DebugMode == True:
                printbtengan()
        # Updates the object variable
        # Update the attribute in the actual plot
        if MinOrMax == "Max":
            if DebugMode == True:
                printbtengan()
        # Updates the object variable
        # Update the attribute in the actual plot

    def UpdateSelectedTheme(ThemeIndex):
        if DebugMode == True:
            printbtengan()
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

    # Signal Colour Button
    self.SignalColour = self.findChild(QPushButton, "SignalColour")
    self.SignalColour.clicked.connect(
        lambda: ChannelLineArr[SignalSelectedIndex].UpdateColour())

    # Updates global variable (SignalSelectedIndex) on combobox change
    self.ChannelsMenu = self.findChild(QComboBox, "ChannelsMenu")
    self.ChannelsMenu.currentIndexChanged.connect(lambda: SetSignalIndex(
        self.ChannelsMenu.currentIndex()))  # on index change

    # # Select Signal Colour Button
    # self.SignalColour = self.findChild(QPushButton, "SignalColour")
    # self.SignalColour.clicked.connect(lambda: printbtengan())

    # Plot
