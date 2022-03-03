
#THIS FILE CONTAINS FUNCTION DEFENITIONS AND OBJECTS USED IN MAIN
#IT WILL BE SPLIT INTO MORE LOGICAL MODULES IN THE FUTURE

import string
from PyQt5 import QtWidgets, uic
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTextEdit, QFileDialog, QScrollBar, QComboBox, QCheckBox
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


def SetSelectedIndex(Input, Selector):
    if Selector == "Signal":
        global SignalSelectedIndex
        SignalSelectedIndex = Input
        printDebug("Signal dropdown: " + str(SignalSelectedIndex))
    if Selector == "Spectro":
        global SpectroSelectedIndex
        SpectroSelectedIndex = Input
        printDebug("Spectrogram dropdown: " + str(SpectroSelectedIndex))



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

        printDebug(str(self.LineColour) + " set as colour for channel: " +
                  str(SignalSelectedIndex))

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

class PlotterWindow:
    def __init__(self, YAxisRange = (0,1), XAxisRange = (-1,1) , CineSpeed = 1 ):
        self.YAxisRange = YAxisRange #Tuple containing min/max ranges
        self.XAxisRange = XAxisRange 

        self.CineSpeed = CineSpeed
        


def printDebug(Value): #Enabled when global debug mode is on
    if DebugMode == 1:
        print(Value)


class ChannelSpectrogram:
    def __init__(self, FreqRangeMax=1000, FreqRangeMin=0, SelectedChannel=1, SelectedTheme="Default"):
        self.FreqRangeMax = FreqRangeMax
        self.FreqRangeMin = FreqRangeMin
        self.SelectedTheme = SelectedTheme

    def UpdateFreqRange(Input, MinOrMax):
        if MinOrMax == "Min":
            if DebugMode == True:
                printDebug("Brengan")
        # Updates the object variable
        # Update the attribute in the actual plot
        if MinOrMax == "Max":
            if DebugMode == True:
                printDebug("Brengan")
        # Updates the object variable
        # Update the attribute in the actual plot

    def UpdateSelectedTheme(ThemeIndex):
        if DebugMode == True:
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

    # Signal Colour Button
    self.SignalColour = self.findChild(QPushButton, "SignalColour")
    self.SignalColour.clicked.connect(
        lambda: ChannelLineArr[SignalSelectedIndex].UpdateColour())

    self.ShowHide = self.findChild(QCheckBox, "ShowHide")
    self.ShowHide.stateChanged.connect(
        lambda: ChannelLineArr[SignalSelectedIndex].UpdateHide())

    # Updates global variable (SignalSelectedIndex) on combobox change
    self.ChannelsMenu = self.findChild(QComboBox, "ChannelsMenu")
    self.ChannelsMenu.currentIndexChanged.connect(lambda: SetSelectedIndex(
        self.ChannelsMenu.currentIndex(),"Signal"))  # on index change

    # Updates SpectroSelectedIndex on change
    self.SpectroMenu = self.findChild(QComboBox, "SpectroMenu")
    self.SpectroMenu.currentIndexChanged.connect(lambda: SetSelectedIndex(
    self.SpectroMenu.currentIndex(), "Spectro")) 
    # Plot
