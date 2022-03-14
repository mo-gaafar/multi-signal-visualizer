from msilib.schema import Directory
from re import A
from PyQt5 import QtWidgets, uic
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTextEdit, QFileDialog, QScrollBar, QComboBox, QColorDialog, QCheckBox, QSlider
from numpy.lib.index_tricks import IndexExpression

import pandas as pd
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

from wfdb.io.record import rdrecord


from PyQt5.QtWidgets import *
from fpdf import FPDF
import wfdb

# LOCAL MODULES
import classes
import interface
import utility as util
import pdf


plt.rcParams['axes.facecolor'] = 'black'
plt.rc('axes', edgecolor='w')
plt.rc('xtick', color='w')
plt.rc('ytick', color='w')
plt.rcParams['savefig.facecolor'] = 'black'
plt.rcParams["figure.autolayout"] = True


DebugMode = False  # Debug mode enables printing


class MainWindow(QtWidgets.QMainWindow):

    def initArrays(self):
        for Index in range(3):
            self.ChannelLineArr.append(classes.ChannelLine())
            print(self.ChannelLineArr[Index])

    # Mainwindow constructor
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('mainwindow.ui', self)

        self.setWindowIcon(QtGui.QIcon('icon.png'))
        # set the title
        self.setWindowTitle("Multi-Channel Signal Viewer")

        # Initialization functions
        interface.initConnectors(self)
        # interfacing.initSpectroRangeSliders(self)
        self.ChannelLineArr = []
        self.initArrays()
        self.CreateSpectrogramFigure()

        self.pointsToAppend = 0
        self.PlotterWindowProp = classes.PlotterWindow()
        self.PauseToggleVar = False
        self.HoldVarH = False
        self.HoldVarV = False
        self.xAxis = [0, 0, 0]
        self.yAxis = [0, 0, 0]

    def Browse(self):
        self.filename = QFileDialog.getOpenFileName(
            None, 'open the signal file', './', filter="Raw Data(*.csv *.txt *.xls *.hea *.dat *.rec)")
        path = self.filename[0]
        util.printDebug("Selected path: " + path)
        self.OpenFile(path)

    def OpenFile(self, path: str):
        TempArrX = []
        TempArrY = []
        self.fsampling = 1
        filetype = path[len(path)-3:]  # gets last 3 letters of path

        if filetype == "hea" or filetype == "rec" or filetype == "dat":
            self.record = wfdb.rdrecord(path[:-4], channels=[0])
            TempArrY = self.record.p_signal
            TempArrY = np.concatenate(TempArrY)

            # print(self.record.fs)
            self.fsampling = self.record.fs
            classes.FreqRangeMax = self.fsampling/2
            # print(TempArrY)

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

        self.ChannelLineArr[classes.SignalSelectedIndex].Filepath = path

        # CHECKS IF CHANNEL 1 ISNT PLOTTED
        if self.ChannelLineArr[0].Filepath == "null":
            QtWidgets.QMessageBox.warning(
                self, 'CHANNEL 1 EMPTY ', 'PLEASE PLOT CHANNEL 1 FIRST')
            self.ChannelLineArr[0].Amplitude = TempArrY
            self.ChannelLineArr[0].Time = TempArrX

        else:
            self.ChannelLineArr[classes.SignalSelectedIndex].Amplitude = TempArrY
            self.ChannelLineArr[classes.SignalSelectedIndex].Time = TempArrX

        self.Legend = self.Plot.addLegend()
        classes.initSpectroRangeSliders(self)

        self.plotSpectro()

        self.plot_data()  # starts plot after file is accessed

    def plot_data(self):

        pen = pg.mkPen(color=(255, 255, 255))
        self.ChannelLineArr[classes.SignalSelectedIndex].PlotWidgetReference = self.Plot.plot(
            pen=self.ChannelLineArr[classes.SignalSelectedIndex].GetColour(), name="Channel " + str(classes.SignalSelectedIndex + 1))
        self.Plot.showGrid(x=True, y=True)

        self.MinSignalLen = len(self.ChannelLineArr[0].Amplitude)
        util.printDebug(
            "Max length of x plots is: " + str(self.MinSignalLen))
        self.pointsToAppend = 0

        # TODO: Set limits based on all plottable signals
        # use object oriented next time....
        MaxX = 0
        MaxY = 0
        MinX = 0
        MinY = 0

        for Index in range(3):  # TODO: make range variable later
            if len(self.ChannelLineArr[Index].Time) != 0 and len(self.ChannelLineArr[Index].Time) > MaxX:
                MaxX = len(self.ChannelLineArr[Index].Time)

            if len(self.ChannelLineArr[Index].Amplitude) != 0 and max(self.ChannelLineArr[Index].Amplitude) > MaxY:
                MaxY = max(self.ChannelLineArr[Index].Amplitude)

            if len(self.ChannelLineArr[Index].Time) != 0 and len(self.ChannelLineArr[Index].Time) < MinX:
                MinX = len(self.ChannelLineArr[Index].Time)

            if len(self.ChannelLineArr[Index].Amplitude) != 0 and min(self.ChannelLineArr[Index].Amplitude) < MinY:
                MinY = min(self.ChannelLineArr[Index].Amplitude)

        # MinY = -1  # Placeholder
        util.printDebug("MaxX: " + str(MaxX))

        self.Plot.plotItem.setLimits(
            xMin=MinX, xMax=MaxX, yMin=MinY, yMax=MaxY)
        self.pointsToAppend = 0  # Plotted Points counter

        self.MinY = MinY
        self.MaxY = MaxY

        # Initialize Qt Timer
        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)  # Overflow timer
        self.timer.timeout.connect(self.update_plot_data)  # Event handler
        self.timer.start()  # Start timer

    # def InitDataPoints(self):

    def update_plot_data(self):

        self.timer.setInterval(self.PlotterWindowProp.CineSpeed)

        for ChannelIndex in range(len(self.ChannelLineArr)):
            # checks if signal has information to be plotted
            # Check if channel contains data (TODO: change this later to a bool)
            if self.ChannelLineArr[ChannelIndex].Filepath != "null":

                # Index of channels containing files
                # self.FilledChannels.append(ChannelIndex)
                self.xAxis[ChannelIndex] = self.ChannelLineArr[ChannelIndex].Time[:self.pointsToAppend]
                self.yAxis[ChannelIndex] = self.ChannelLineArr[ChannelIndex].Amplitude[:self.pointsToAppend]

        self.pointsToAppend += 5

        self.horizontalScrollBarFunction()
        self.verticalScrollBarFunction()
        # interfacing.printDebug("Minimum signal length: " + str(MinSignalLen))
        if self.pointsToAppend > self.MinSignalLen:
            self.timer.stop()
            QtWidgets.QMessageBox.warning(
                self, 'NO SIGNAL ', 'The signal duration has ended')

        # Plots all signals
        for Index in range(3):  # TODO: make this variable later.;
            if self.ChannelLineArr[Index].Filepath != "null" and len(self.ChannelLineArr[Index].Time) > self.pointsToAppend:
                # TODO: signal should be time indexed
                self.ChannelLineArr[Index].PlotWidgetReference.setData(
                    self.xAxis[0], self.yAxis[Index], pen=self.ChannelLineArr[Index].GetColour(), name="name")

    def DynamicUpdate(self):
        for Index in range(3):  # TODO: make this variable later
            if self.ChannelLineArr[Index].Filepath != "null" and len(self.ChannelLineArr[Index].Time) > self.pointsToAppend:
                if self.ChannelLineArr[Index].IsHidden == True:
                    self.ChannelLineArr[Index].PlotWidgetReference.hide(
                    )
                else:
                    self.ChannelLineArr[Index].PlotWidgetReference.show(
                    )

                self.ChannelLineArr[Index].PlotWidgetReference.setData(
                    self.xAxis[0], self.yAxis[Index], pen=self.ChannelLineArr[Index].GetColour(), name=self.ChannelLineArr[Index].Label, skipFiniteCheck=True)

    def SelectSignalColour(self):
        self.ChannelLineArr[classes.SignalSelectedIndex].UpdateColour(
            QColorDialog.getColor().name())
        self.DynamicUpdate()

    def ZoomInFunction(self):
        self.timer.stop()  # Stopping the signal in order to view a specific point
        # setting the toggle to true in order to press play to continue plotting
        self.PauseToggleVar = True
        self.Plot.plotItem.getViewBox().scaleBy((0.5, 0.5))
        util.printDebug("Zoomin")

    def ZoomOutFunction(self):
        self.timer.stop()
        self.PauseToggleVar = True
        self.Plot.plotItem.getViewBox().scaleBy((1.5, 1.5))
        util.printDebug("Zoomout")

    def TogglePause(self):
        self.PauseToggleVar = not self.PauseToggleVar  # On click, toggle state
        if self.PauseToggleVar == True:
            self.timer.stop()

        else:
            self.timer.start()
        util.printDebug("PauseToggle")
        # self.DynamicUpdate()

    def ToggleHide(self, Checked):
        self.ChannelLineArr[classes.SignalSelectedIndex].IsHidden = Checked
        self.DynamicUpdate()

    def IsHeldH(self):
        self.HoldVarH = True  # mamsoka

    def NotHeldH(self):
        self.HoldVarH = False  # etsabet

    def IsHeldV(self):
        self.HoldVarV = True  # mamsoka

    def NotHeldV(self):
        self.HoldVarV = False  # etsabet

    def horizontalScrollBarFunction(self):

        self.ValueHorizontal = self.horizontalScrollBar.value()

        if self.HoldVarH == True and self.ValueHorizontal <= self.pointsToAppend:
            self.Plot.plotItem.setXRange(
                self.ChannelLineArr[0].Time[self.ValueHorizontal]-1.0, self.ChannelLineArr[0].Time[self.ValueHorizontal])
        else:
            self.Plot.plotItem.setXRange(
                max(self.xAxis[0], default=0)-1.0, max(self.xAxis[0], default=0))
            # self.ValueHorizontal = self.horizontalScrollBar.setValue(max(self.xAxis[0], default=0)*2000)

        self.horizontalScrollBar.setMinimum(0)
        self.horizontalScrollBar.setMaximum(
            len(self.ChannelLineArr[0].Time))
        self.horizontalScrollBar.setSingleStep(20)

        util.printDebug("Horizontal Scroll: " +
                        str(self.ValueHorizontal))

    def verticalScrollBarFunction(self):
        self.ValueVertical = self.verticalScrollBar.value()

        self.verticalScrollBar.setMinimum(0)
        self.verticalScrollBar.setMaximum(
            len(self.ChannelLineArr[0].Amplitude))
        self.verticalScrollBar.setSingleStep(20)
        # TODO: after Setting limits based on all plottable signals
        # we will have the max and min of y axis
        # by subtracting them we get the length of y axis
        MaxY = self.MaxY
        MinY = self.MinY
        MyRange = (MaxY-MinY)/5
        # law al value beta3 al scroll et8ayar dah ma3nah ano 3aiz maymshesh ma3a al line
        if self.HoldVarV == True:
            # len(self.ChannelLineArr[0].Amplitude) will be replaced with number of points on the plot
            if self.ValueVertical >= 0 and self.ValueVertical <= len(self.ChannelLineArr[0].Amplitude)*(1/5):
                # in order to get the max number of values
                # TAKECARE:hasabat al range hena (n)
                self.Plot.plotItem.setYRange(MaxY-MyRange, MaxY)
            elif self.ValueVertical >= len(self.ChannelLineArr[0].Amplitude)*(1/5) and self.ValueVertical <= len(self.ChannelLineArr[0].Amplitude)*(2/5):

                self.Plot.plotItem.setYRange(MaxY-MyRange*2, MaxY-MyRange)

            elif self.ValueVertical >= len(self.ChannelLineArr[0].Amplitude)*(2/5) and self.ValueVertical <= len(self.ChannelLineArr[0].Amplitude)*(3/5):
                self.Plot.plotItem.setYRange(MaxY-MyRange*3, MaxY-MyRange*2)

            elif self.ValueVertical >= len(self.ChannelLineArr[0].Amplitude)*(3/5) and self.ValueVertical <= len(self.ChannelLineArr[0].Amplitude)*(4/5):
                self.Plot.plotItem.setYRange(MaxY-MyRange*4, MaxY-MyRange*3)
            else:
                self.Plot.plotItem.setYRange(MinY, MaxY-MyRange*4)

        else:
            self.Plot.plotItem.setYRange(min(self.yAxis[0], default=0), max(
                self.yAxis[0], default=0))  # we might need to make the range const
            self.ValueVertical = self.verticalScrollBar.setValue(
                0)  # at amplitude=0

        util.printDebug("Vertical Scroll: " + str(self.ValueVertical))

    def SpeedSliderFunction(self, Input):
        self.ValueCineSpeed = Input
        util.printDebug("Speed Slider: " + str(self.ValueCineSpeed))
        self.PlotterWindowProp.UpdateCineSpeed(Input)
        return self.ValueCineSpeed

    def EditLabelFunction(self, Input):
        self.ChannelLineArr[classes.SignalSelectedIndex].Label = Input
        print(
            self.ChannelLineArr[classes.SignalSelectedIndex].Label)
        self.Legend.getLabel(
            self.ChannelLineArr[classes.SignalSelectedIndex].PlotWidgetReference).setText(Input)

#------------------------------------------------------SPECTROGRAM FUNCTIONS------------------------------------------------------------------------------------#

    def CreateSpectrogramFigure(self):
        self.figure = plt.figure()                     # Create matplotlib fig
        self.figure.patch.set_facecolor('black')
        self.axes = self.figure.add_subplot()
        self.Spectrogram = Canvas(self.figure)
        self.SpectrogramBox_2.addWidget(self.Spectrogram)

    def plotSpectro(self):

        FS = 250

        # Corner Case Of Empty Channel
        if len(self.ChannelLineArr[classes.SpectroSelectedIndex].Amplitude) == 0:
            self.axes.clear()
            self.Spectrogram.draw()
            self.figure.canvas.draw()

        else:
            if self.fsampling != 1:
                FS = self.fsampling

            self.SignalArray = np.array(
                self.ChannelLineArr[classes.SpectroSelectedIndex].Amplitude)
            self.freq, self.time, self.Sxx = signal.spectrogram(
                self.SignalArray, fs=FS, window='hanning', nperseg=128, noverlap=64, detrend=False, mode='magnitude', scaling='density')

            self.max_freq = np.max(self.freq)
            self.axes.set_ylim([0, self.max_freq])

            # Slices freq arr into range specified by sliders
            self.freqRange = np.where((self.freq >= classes.FreqRangeMin) & (
                self.freq <= classes.FreqRangeMax))
            self.freq = self.freq[self.freqRange]
            self.Sxx = self.Sxx[self.freqRange, :][0]

            # Plots Spectrogram
            self.axes.pcolormesh(
                self.time, self.freq, 10*np.log10(self.Sxx), cmap=classes.SpectroTheme)
            self.axes.set_ylabel('Frequency [Hz]', color='white')
            self.axes.set_xlabel('Time [s]', color='white')
            self.axes.set_yscale('symlog')

            self.Spectrogram.draw()
            self.figure.canvas.draw()
# Making a picture of the spectrogram to use it the pdf
            plt.savefig('Spectrogram.png')

    def SetSpectroSelectedIndex(self, Input):
        classes.SpectroSelectedIndex = Input
        self.plotSpectro()

    def SetSpectroTheme(self, Input):
        classes.SpectroTheme = Input
        self.plotSpectro()

    def SpectrogramFrequency(self, Input, MinOrMax):
        if MinOrMax == "min":
            if Input < classes.FreqRangeMax:
                classes.FreqRangeMin = Input
            else:
                # Prevents min from exceeding max
                self.MinRangeSlider.setValue(classes.FreqRangeMin)
        if MinOrMax == "max":
            if Input > classes.FreqRangeMin:
                classes.FreqRangeMax = Input
            else:
                # Prevents max from going below min
                self.MaxRangeSlider.setValue(classes.FreqRangeMax)

        self.plotSpectro()
        util.printDebug(MinOrMax + "SpectroSlider: " + str(Input))

#--------------------------------------------------------EXPORT FUNCTION---------------------------------------------------------------------------#

    def ExportPDF(self):
        pdf.Exporter(self)

#------------------------------------------------------------------------------------------------------------------------------------------------------#


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
