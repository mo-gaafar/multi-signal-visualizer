from msilib.schema import Directory
from tkinter import Label, dialog
from tkinter.tix import DirSelectDialog
from PyQt5 import QtWidgets, uic
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTextEdit, QFileDialog, QScrollBar, QComboBox, QColorDialog, QCheckBox, QSlider
from numpy.lib.index_tricks import IndexExpression

from pyqtgraph import PlotWidget
import pyqtgraph as pg
import sys
import csv
import os
from random import randint

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
import scipy.io
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import time

from wfdb.io.record import rdrecord

import interfacing  # local module
import wfdb


plt.rcParams['axes.facecolor'] = 'black'
plt.rc('axes', edgecolor='w')
plt.rc('xtick', color='w')
plt.rc('ytick', color='w')
plt.rcParams['savefig.facecolor'] = 'black'
plt.rcParams["figure.autolayout"] = True


DebugMode = False  # Debug mode enables printing


class MainWindow(QtWidgets.QMainWindow):

    # Mainwindow constructor
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('mainwindow2.ui', self)

        # Initialization functions
        interfacing.initConnectors(self)
        #interfacing.initSpectroRangeSliders(self)
        interfacing.initArrays(self)
        self.CreateSpectrogramFigure()

        self.PlotterWindowProp = interfacing.PlotterWindow()
        self.PauseToggleVar = False

        self.xAxis = [0, 0, 0]
        self.yAxis = [0, 0, 0]

        self.LineReferenceArr = [self.Plot.plot(self.xAxis, self.yAxis), self.Plot.plot(
            self.xAxis, self.yAxis), self.Plot.plot(self.xAxis, self.yAxis)]

    def Browse(self):
        self.filename = QFileDialog.getOpenFileName(
            None, 'open the signal file', './', filter="Raw Data(*.csv *.txt *.xls *.hea *.dat *.rec)")
        path = self.filename[0]
        interfacing.printDebug("Selected path: " + path)
        self.OpenFile(path)

    def OpenFile(self, path: str):
        TempArrX = []
        TempArrY = []
        self.fsampling = 0
        filetype = path[len(path)-3:]  # gets last 3 letters of path

        if filetype == "hea" or filetype == "rec" or filetype == "dat":
            self.record = wfdb.rdrecord(path[:-4], channels=[1])
            #self.d_signal = self.record.adc()
            #TempArrX = self.d_signal[:][1]
            TempArrY = self.record.p_signal
            TempArrY = np.concatenate(TempArrY)
            #print(self.record.fs)
            self.fsampling = self.record.fs
            interfacing.FreqRangeMax = self.fsampling/2
            #print(TempArrY)
            for Index in range(len(TempArrY)):
                TempArrX.append(Index/self.record.fs)

        if filetype == "csv" or filetype == "txt" or filetype == "xls":
            with open(path, 'r') as csvFile:    # 'r' its a mode for reading and writing
                csvReader = csv.reader(csvFile, delimiter=',')
                for line in csvReader:
                    TempArrY.append(
                        float(line[1]))
                    TempArrX.append(
                        float(line[0]))

        interfacing.ChannelLineArr[interfacing.SignalSelectedIndex].Amplitude = TempArrY
        interfacing.ChannelLineArr[interfacing.SignalSelectedIndex].Time = TempArrX
        interfacing.ChannelLineArr[interfacing.SignalSelectedIndex].Filepath = path

        interfacing.initSpectroRangeSliders(self)
        self.plotSpectro()

        self.plot_data()  # starts plot after file is accessed

    def plot_data(self):

        pen = pg.mkPen(color=(255, 255, 255))
        self.PlotWidget = self.Plot.plot(pen=pen)
        self.Plot.showGrid(x=True, y=True)
        self.Plot.addLegend()

        self.MinSignalLen = len(interfacing.ChannelLineArr[0].Amplitude)
        interfacing.printDebug(
            "Max length of x plots is: " + str(self.MinSignalLen))
        self.pointsToAppend = 0

        # TODO: Set limits based on all plottable signals

        MaxX = 0
        MaxY = 0

        for Index in range(3):
            if len(interfacing.ChannelLineArr[Index].Time) != 0 and len(interfacing.ChannelLineArr[Index].Time) > MaxX:
                MaxX = len(interfacing.ChannelLineArr[Index].Time)

            if len(interfacing.ChannelLineArr[Index].Amplitude) != 0 and len(interfacing.ChannelLineArr[Index].Time) > MaxY:
                MaxY = len(interfacing.ChannelLineArr[Index].Amplitude)

        #interfacing.printDebug("MaxY = " + str(MaxY))
        # self.Plot.plotItem.setLimits(xMin=min(self.time), xMax=max(self.time), yMin=min(
        #     self.amplitude), yMax=max(self.amplitude))  # limit bata3 al axis ali 3andi
        MinY = -1  # Placeholder
        interfacing.printDebug("MaxX: " + str(MaxX))
        # limit bata3 al axis ali 3andi
        self.Plot.plotItem.setLimits(xMin=0, xMax=MaxX, yMin=MinY, yMax=MaxY)
        self.pointsToAppend = 0  # Plotted Points counter

        # Initialize Qt Timer
        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)  # Overflow timer
        self.timer.timeout.connect(self.update_plot_data)  # Event handler
        self.timer.start()  # Start timer

    # def InitDataPoints(self):

    def update_plot_data(self):
        #print("Timer ", self.timer.interval())
        self.timer.setInterval(self.PlotterWindowProp.CineSpeed)

        for ChannelIndex in range(len(interfacing.ChannelLineArr)):
            # checks if signal has information to be plotted
            # Check if channel contains data (TODO: change this later to a bool)
            if interfacing.ChannelLineArr[ChannelIndex].Filepath != "null":

                # Index of channels containing files
                # self.FilledChannels.append(ChannelIndex)

                self.xAxis[ChannelIndex] = interfacing.ChannelLineArr[ChannelIndex].Time[:self.pointsToAppend]
                self.yAxis[ChannelIndex] = interfacing.ChannelLineArr[ChannelIndex].Amplitude[:self.pointsToAppend]

        # interfacing.printDebug(self.xAxis[0])
        self.pointsToAppend += 5
        # if self.pointsToAppend > len(self.time):
        #     self.timer.stop()
        # TODO: if the shortest signal ends stop the timer
        #MinSignalLen = min(map(len, interfacing.ChannelLineArr.Time))

        # DEBUGGING LOOP
        for Index in range(3):
            if interfacing.ChannelLineArr[Index].Filepath != "null":
                interfacing.printDebug("Channel number: " + str(Index))
                interfacing.printDebug(
                    len(interfacing.ChannelLineArr[Index].Time))
                interfacing.printDebug(len(self.xAxis[Index]))

        #interfacing.printDebug("Minimum signal length: " + str(MinSignalLen))
        if self.pointsToAppend > self.MinSignalLen:
            self.timer.stop()

        # if self.time[self.pointsToAppend] > 1:   #1 because this where our axis stops at at the begings to evry time we need to update the axis inorder for it to plot dynamiclly
        # self.Plot.setLimits(xMax=max(self.x, default=0))

        # TODO: Set y limits based on all plottable signals
        # TODO: Zoom and scrolling might require changes to limits

        # TODO: to be embedded as in the class plotwindow
        # VisibleYRange = (0,0)
        # VisibleXRange = (0,0)

        # TODO: fix this
        self.Plot.plotItem.setXRange(
            max(self.xAxis[0], default=0)-1.0, max(self.xAxis[0], default=0))

        # Plots all signals
        for Index in range(3):  # TODO: make this variable later
            if interfacing.ChannelLineArr[Index].Filepath != "null":
                # TODO: signal should be time indexed
                # self.PlotWidget.setData(
                # self.xAxis[0], self.yAxis[Index], pen=interfacing.ChannelLineArr[Index].GetColour(), skipFiniteCheck=True)
                self.LineReferenceArr[Index].setData(
                    self.xAxis[0], self.yAxis[Index], pen=interfacing.ChannelLineArr[Index].GetColour(), skipFiniteCheck=True)

    def ExportPDF(self):
        # Folder Dialog (failed attempt)
        QFileDialog.setFileMode(self, Directory)
        QFileDialog.setOption(self, DirSelectDialog)
        self.filename = QFileDialog.getOpenFileName()
        interfacing.printDebug(self.filename)
        # @Abdullahsaeed2 etfaddal hena

        # Step 1 choose folder location
        # Step 2 create snapshot of plotter
        # Step 3 create report with required variables and formatting
        # Step 4 save in selected folder location (step 1)

    # OPENS COLOUR DIALOG WHEN BUTTON IS PRESSED
    def SelectSignalColour(self):
        self.SignalColour = QColorDialog.getColor().name()
        return self.SignalColour

    def ZoomInFunction(self):
        interfacing.printDebug("Zoomin")

    def ZoomOutFunction(self):
        interfacing.printDebug("Zoomout")

    def TogglePause(self):
        self.PauseToggleVar = not self.PauseToggleVar  # On click, toggle state
        if self.PauseToggleVar == True:
            self.timer.stop()
        else:
            self.timer.start()
        interfacing.printDebug("PauseToggle")

    def horizontalScrollBarFunction(self, Input):
        self.ValueHorizontal = Input
        interfacing.printDebug("Horizontal Scroll: " +
                               str(self.ValueHorizontal))

    def verticalScrollBarFunction(self, Input):
        self.ValueVertical = Input
        interfacing.printDebug("Vertical Scroll: " + str(self.ValueVertical))

    def SpeedSliderFunction(self, Input):
        self.ValueCineSpeed = Input
        interfacing.printDebug("Speed Slider: " + str(self.ValueCineSpeed))
        self.PlotterWindowProp.UpdateCineSpeed(Input)
        return self.ValueCineSpeed


#------------------------------------------------------SPECTROGRAM FUNCTIONS------------------------------------------------------------------------------------#

    def CreateSpectrogramFigure(self):
        self.figure = plt.figure()                     # Create matplotlib fig
        self.figure.patch.set_facecolor('black')
        self.axes = self.figure.add_subplot()
        self.Spectrogram = Canvas(self.figure)
        self.SpectrogramBox_2.addWidget(self.Spectrogram)

    def plotSpectro(self):

        FS = 0

        # Corner Case Of Empty Channel
        if len(interfacing.ChannelLineArr[interfacing.SpectroSelectedIndex].Amplitude) == 0:
            self.axes.clear()
            self.Spectrogram.draw()
            self.figure.canvas.draw()

        else:
            if self.fsampling != 0:
                FS = self.fsampling

            self.SignalArray = np.array(
                interfacing.ChannelLineArr[interfacing.SpectroSelectedIndex].Amplitude)
            self.freq, self.time, self.Sxx = signal.spectrogram(
                self.SignalArray, fs=FS, window='hanning', nperseg=128, noverlap=64, detrend=False, mode='magnitude', scaling='density')

            self.max_freq = np.max(self.freq)
            self.axes.set_ylim([0, self.max_freq])

            # Slices freq arr into range specified by sliders
            self.freqRange = np.where((self.freq >= interfacing.FreqRangeMin) & (self.freq <= interfacing.FreqRangeMax))
            self.freq = self.freq[self.freqRange]
            self.Sxx = self.Sxx[self.freqRange, :][0]

            # Plots Spectrogram
            self.axes.pcolormesh(self.time, self.freq, 10*np.log10(self.Sxx), cmap = interfacing.SpectroTheme)
            self.axes.set_ylabel('Frequency [Hz]', color = 'white')
            self.axes.set_xlabel('Time [s]', color = 'white')
            self.axes.set_yscale('symlog')
            self.Spectrogram.draw()
            self.figure.canvas.draw()

    def SetSpectroSelectedIndex(self, Input):
        interfacing.SpectroSelectedIndex = Input
        self.plotSpectro()

    def SetSpectroTheme(self, Input):
        interfacing.SpectroTheme = Input
        self.plotSpectro()

    def SpectrogramFrequency(self, Input, MinOrMax):
        if MinOrMax == "min":
            if Input < interfacing.FreqRangeMax:
                interfacing.FreqRangeMin = Input
            else:
                self.MinRangeSlider.setValue(interfacing.FreqRangeMin)  # Prevents min from exceeding max
        if MinOrMax == "max":
            if Input > interfacing.FreqRangeMin:
                interfacing.FreqRangeMax = Input
            else:
                self.MaxRangeSlider.setValue(interfacing.FreqRangeMax)  # Prevents max from going below min

        self.plotSpectro()
        interfacing.printDebug(MinOrMax + "SpectroSlider: " + str(Input))

#------------------------------------------------------------------------------------------------------------------------------------------------------#


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


# BASIC CODE TO TEST WHETHER PYQTGRAPH WIDGET LOADS
