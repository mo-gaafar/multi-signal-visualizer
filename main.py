from msilib.schema import Directory
from re import A
from tkinter import Label, dialog
from tkinter.tix import DirSelectDialog
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
import time

from wfdb.io.record import rdrecord

import pyqtgraph.exporters
import pandas
import statistics
from PyQt5.QtWidgets import *
from fpdf import FPDF
from pyqtgraph.GraphicsScene import exportDialog
# from PDF import PDF
import pyqtgraph.exporters
# import shutil
# import datetime
# from PyQt5.QtGui import *
# from PyQt5.QtCore import *
# from PyQt5.QtWidgets import *

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

        self.setWindowIcon(QtGui.QIcon('icon.png'))
        # set the title
        self.setWindowTitle("Multi-Channel Signal Viewer")

        # Initialization functions
        interfacing.initConnectors(self)
        # interfacing.initSpectroRangeSliders(self)
        interfacing.initArrays(self)
        self.CreateSpectrogramFigure()

        self.PlotterWindowProp = interfacing.PlotterWindow()
        self.PauseToggleVar = False
        self.HoldVarH = False
        self.HoldVarV = False
        self.xAxis = [0, 0, 0]
        self.yAxis = [0, 0, 0]
        self.PlotWidget = []
        for Index in range(3):
            self.PlotWidget.append(PlotWidget())

        self.LineReferenceArr = [self.Plot.plot(self.xAxis, self.yAxis), self.Plot.plot(
            self.xAxis, self.yAxis), self.Plot.plot(self.xAxis, self.yAxis)]

        # new Variables ABDULLAH
        self.amplitude = [[], [], []]
        self.time = [[], [], []]
        self.pointsToAppend = 0
        # a list of images of the graphs (use for create_pdf)
        self.list = []
        # a list of images of the spectrograms (use for create_pdf)
        self.spectroImg_list = [None]

    def Browse(self):
        self.filename = QFileDialog.getOpenFileName(
            None, 'open the signal file', './', filter="Raw Data(*.csv *.txt *.xls *.hea *.dat *.rec)")
        path = self.filename[0]
        interfacing.printDebug("Selected path: " + path)
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
            interfacing.FreqRangeMax = self.fsampling/2
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

        interfacing.ChannelLineArr[interfacing.SignalSelectedIndex].Filepath = path

        # CHECKS IF CHANNEL 1 ISNT PLOTTED
        if interfacing.ChannelLineArr[0].Filepath == "null":
            QtWidgets.QMessageBox.warning(
                self, 'CHANNEL 1 EMPTY ', 'PLEASE PLOT CHANNEL 1 FIRST')
            interfacing.ChannelLineArr[0].Amplitude = TempArrY
            interfacing.ChannelLineArr[0].Time = TempArrX

        else:
            interfacing.ChannelLineArr[interfacing.SignalSelectedIndex].Amplitude = TempArrY
            interfacing.ChannelLineArr[interfacing.SignalSelectedIndex].Time = TempArrX

        self.Legend = self.Plot.addLegend()
        interfacing.initSpectroRangeSliders(self)

        self.plotSpectro()

        self.plot_data()  # starts plot after file is accessed

    def plot_data(self):

        pen = pg.mkPen(color=(255, 255, 255))
        self.PlotWidget[interfacing.SignalSelectedIndex] = self.Plot.plot(
            pen=interfacing.ChannelLineArr[interfacing.SignalSelectedIndex].GetColour(), name="Channel " + str(interfacing.SignalSelectedIndex + 1))
        self.Plot.showGrid(x=True, y=True)

        self.MinSignalLen = len(interfacing.ChannelLineArr[0].Amplitude)
        interfacing.printDebug(
            "Max length of x plots is: " + str(self.MinSignalLen))
        self.pointsToAppend = 0

        # TODO: Set limits based on all plottable signals
        # use object oriented next time....
        MaxX = 0
        MaxY = 0
        MinX = 0
        MinY = 0

        for Index in range(3):  # TODO: make range variable later
            if len(interfacing.ChannelLineArr[Index].Time) != 0 and len(interfacing.ChannelLineArr[Index].Time) > MaxX:
                MaxX = len(interfacing.ChannelLineArr[Index].Time)

            if len(interfacing.ChannelLineArr[Index].Amplitude) != 0 and max(interfacing.ChannelLineArr[Index].Amplitude) > MaxY:
                MaxY = max(interfacing.ChannelLineArr[Index].Amplitude)

            if len(interfacing.ChannelLineArr[Index].Time) != 0 and len(interfacing.ChannelLineArr[Index].Time) < MinX:
                MinX = len(interfacing.ChannelLineArr[Index].Time)

            if len(interfacing.ChannelLineArr[Index].Amplitude) != 0 and min(interfacing.ChannelLineArr[Index].Amplitude) < MinY:
                MinY = min(interfacing.ChannelLineArr[Index].Amplitude)

        # MinY = -1  # Placeholder
        interfacing.printDebug("MaxX: " + str(MaxX))

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

        for ChannelIndex in range(len(interfacing.ChannelLineArr)):
            # checks if signal has information to be plotted
            # Check if channel contains data (TODO: change this later to a bool)
            if interfacing.ChannelLineArr[ChannelIndex].Filepath != "null":

                # Index of channels containing files
                # self.FilledChannels.append(ChannelIndex)
                self.xAxis[ChannelIndex] = interfacing.ChannelLineArr[ChannelIndex].Time[:self.pointsToAppend]
                self.yAxis[ChannelIndex] = interfacing.ChannelLineArr[ChannelIndex].Amplitude[:self.pointsToAppend]

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
            if interfacing.ChannelLineArr[Index].Filepath != "null" and len(interfacing.ChannelLineArr[Index].Time) > self.pointsToAppend:
                # TODO: signal should be time indexed
                # self.PlotWidget.setData(
                # self.xAxis[0], self.yAxis[Index], pen=interfacing.ChannelLineArr[Index].GetColour(), skipFiniteCheck=True)
                self.LineReferenceArr[Index].setData(
                    self.xAxis[0], self.yAxis[Index], pen=interfacing.ChannelLineArr[Index].GetColour(), name="name")


#-----------------------------------------------------------------------------------------------------------------------------------------------#
    # OPENS COLOUR DIALOG WHEN BUTTON IS PRESSED

    def DynamicUpdate(self):
        for Index in range(3):  # TODO: make this variable later
            if interfacing.ChannelLineArr[Index].Filepath != "null" and len(interfacing.ChannelLineArr[Index].Time) > self.pointsToAppend:
                if interfacing.ChannelLineArr[Index].IsHidden == True:
                    self.LineReferenceArr[Index].hide()
                else:
                    self.LineReferenceArr[Index].show()

                self.LineReferenceArr[Index].setData(
                    self.xAxis[0], self.yAxis[Index], pen=interfacing.ChannelLineArr[Index].GetColour(), name=interfacing.ChannelLineArr[Index].Label, skipFiniteCheck=True)

    def SelectSignalColour(self):
        self.SignalColour = QColorDialog.getColor().name()
        return self.SignalColour

    def ZoomInFunction(self):
        self.timer.stop()  # Stopping the signal in order to view a specific point
        # setting the toggle to true in order to press play to continue plotting
        self.PauseToggleVar = True
        self.Plot.plotItem.getViewBox().scaleBy((0.5, 0.5))
        interfacing.printDebug("Zoomin")

    def ZoomOutFunction(self):
        self.timer.stop()
        self.PauseToggleVar = True
        self.Plot.plotItem.getViewBox().scaleBy((1.5, 1.5))
        interfacing.printDebug("Zoomout")

    def TogglePause(self):
        self.PauseToggleVar = not self.PauseToggleVar  # On click, toggle state
        if self.PauseToggleVar == True:
            self.timer.stop()

        else:
            self.timer.start()
        interfacing.printDebug("PauseToggle")
        # self.DynamicUpdate()

    def ToggleHide(self, Checked):
        interfacing.ChannelLineArr[interfacing.SignalSelectedIndex].IsHidden = Checked
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
                interfacing.ChannelLineArr[0].Time[self.ValueHorizontal]-1.0, interfacing.ChannelLineArr[0].Time[self.ValueHorizontal])
        else:
            self.Plot.plotItem.setXRange(
                max(self.xAxis[0], default=0)-1.0, max(self.xAxis[0], default=0))
            # self.ValueHorizontal = self.horizontalScrollBar.setValue(max(self.xAxis[0], default=0)*2000)

        self.horizontalScrollBar.setMinimum(0)
        self.horizontalScrollBar.setMaximum(
            len(interfacing.ChannelLineArr[0].Time))
        self.horizontalScrollBar.setSingleStep(20)

        interfacing.printDebug("Horizontal Scroll: " +
                               str(self.ValueHorizontal))

    def verticalScrollBarFunction(self):
        self.ValueVertical = self.verticalScrollBar.value()

        self.verticalScrollBar.setMinimum(0)
        self.verticalScrollBar.setMaximum(
            len(interfacing.ChannelLineArr[0].Amplitude))
        self.verticalScrollBar.setSingleStep(20)
        # TODO: after Setting limits based on all plottable signals
        # we will have the max and min of y axis
        # by subtracting them we get the length of y axis
        MaxY = self.MaxY
        MinY = self.MinY
        MyRange = (MaxY-MinY)/5
        # law al value bata3 al scroll at8yar dah ma3nah ano 3aiz maymshesh ma3a al line
        if self.HoldVarV == True:
            # len(interfacing.ChannelLineArr[0].Amplitude) will be replaced with number of points on the plot
            if self.ValueVertical >= 0 and self.ValueVertical <= len(interfacing.ChannelLineArr[0].Amplitude)*(1/5):
                # in order to get the max number of values
                # TAKECARE:hasabat al range hena (n)
                self.Plot.plotItem.setYRange(MaxY-MyRange, MaxY)
            elif self.ValueVertical >= len(interfacing.ChannelLineArr[0].Amplitude)*(1/5) and self.ValueVertical <= len(interfacing.ChannelLineArr[0].Amplitude)*(2/5):

                self.Plot.plotItem.setYRange(MaxY-MyRange*2, MaxY-MyRange)

            elif self.ValueVertical >= len(interfacing.ChannelLineArr[0].Amplitude)*(2/5) and self.ValueVertical <= len(interfacing.ChannelLineArr[0].Amplitude)*(3/5):
                self.Plot.plotItem.setYRange(MaxY-MyRange*3, MaxY-MyRange*2)

            elif self.ValueVertical >= len(interfacing.ChannelLineArr[0].Amplitude)*(3/5) and self.ValueVertical <= len(interfacing.ChannelLineArr[0].Amplitude)*(4/5):
                self.Plot.plotItem.setYRange(MaxY-MyRange*4, MaxY-MyRange*3)
            else:
                self.Plot.plotItem.setYRange(MinY, MaxY-MyRange*4)

        else:
            self.Plot.plotItem.setYRange(min(self.yAxis[0], default=0), max(
                self.yAxis[0], default=0))  # we might need to make the range const
            self.ValueVertical = self.verticalScrollBar.setValue(
                0)  # at amplitude=0

        interfacing.printDebug("Vertical Scroll: " + str(self.ValueVertical))

    def SpeedSliderFunction(self, Input):
        self.ValueCineSpeed = Input
        interfacing.printDebug("Speed Slider: " + str(self.ValueCineSpeed))
        self.PlotterWindowProp.UpdateCineSpeed(Input)
        return self.ValueCineSpeed

    def EditLabelFunction(self, Input):
        interfacing.ChannelLineArr[interfacing.SignalSelectedIndex].Label = Input
        print(
            interfacing.ChannelLineArr[interfacing.SignalSelectedIndex].Label)
        self.Legend.getLabel(
            self.PlotWidget[interfacing.SignalSelectedIndex]).setText(Input)

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
        if len(interfacing.ChannelLineArr[interfacing.SpectroSelectedIndex].Amplitude) == 0:
            self.axes.clear()
            self.Spectrogram.draw()
            self.figure.canvas.draw()

        else:
            if self.fsampling != 1:
                FS = self.fsampling

            self.SignalArray = np.array(
                interfacing.ChannelLineArr[interfacing.SpectroSelectedIndex].Amplitude)
            self.freq, self.time, self.Sxx = signal.spectrogram(
                self.SignalArray, fs=FS, window='hanning', nperseg=128, noverlap=64, detrend=False, mode='magnitude', scaling='density')

            self.max_freq = np.max(self.freq)
            self.axes.set_ylim([0, self.max_freq])

            # Slices freq arr into range specified by sliders
            self.freqRange = np.where((self.freq >= interfacing.FreqRangeMin) & (
                self.freq <= interfacing.FreqRangeMax))
            self.freq = self.freq[self.freqRange]
            self.Sxx = self.Sxx[self.freqRange, :][0]

            # Plots Spectrogram
            self.axes.pcolormesh(
                self.time, self.freq, 10*np.log10(self.Sxx), cmap=interfacing.SpectroTheme)
            self.axes.set_ylabel('Frequency [Hz]', color='white')
            self.axes.set_xlabel('Time [s]', color='white')
            self.axes.set_yscale('symlog')

            self.Spectrogram.draw()
            self.figure.canvas.draw()
# Making a picture of the spectrogram to use it the pdf
            plt.savefig('Spectrogram.png')

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
                # Prevents min from exceeding max
                self.MinRangeSlider.setValue(interfacing.FreqRangeMin)
        if MinOrMax == "max":
            if Input > interfacing.FreqRangeMin:
                interfacing.FreqRangeMax = Input
            else:
                # Prevents max from going below min
                self.MaxRangeSlider.setValue(interfacing.FreqRangeMax)

        self.plotSpectro()
        interfacing.printDebug(MinOrMax + "SpectroSlider: " + str(Input))
#--------------------------------------------------------RXPORT FUNCTION---------------------------------------------------------------------------#

    def ExportPDF(self):
        # the function that creates the pdf report
        if self.pointsToAppend == 0:
            QtWidgets.QMessageBox.warning(
                self, 'NO SIGNAL ', 'You have to plot a signal first')
        else:
            pdname = QFileDialog.getSaveFileName(
                None, str('Save the signal file'), None, str("PDF FIles(*.pdf)"))
            if pdname != '':
                pdf = FPDF()
                # set pdf title
                pdf.add_page()
                pdf.set_font('Arial', 'B', 17)
                pdf.cell(70)

                pdf.cell(50, 10, 'Signal Viewer Report', 0, 0, 'C')
                pdf.ln(5)
            # pdf.cell(60, 10, 'Abdullah', 0, 0, 'L')

                pdf.ln(20)
            # create a CSV file of the signal
                ex1 = pg.exporters.CSVExporter(self.Plot.plotItem)
                ex1.export('test.csv')

                df = pd.read_csv('test.csv')
                self.r = df.describe().loc[['mean', 'min']]
                self.p = df.describe().loc[['max', 'std']]

                self.E = df.describe()
            #   print(self.E)
                # pdf.cell(50, 10, self.E, 0, 0, 'C')

        # create a excell sheet of the signal

                ex2 = pg.exporters.SVGExporter(self.Plot.plotItem)
                ex2.export('test.svg')
        # create a picture of the signal
                ex3 = pg.exporters.ImageExporter(self.Plot.plotItem)
                ex3.export('test.png')
        # put the picture of the signal in an array
                self.list = ['test.png']
        # call the function create_pdf()
                # put the graphs on the pdf
                pdf.image('Desgin/CUFE.png', 1, 1, 50, 40)
                pdf.image('Desgin/logo.png', 160, 1, 50, 40)
                pdf.image('test.png', 40, 50, 150, 100)
                pdf.image('Spectrogram.png', 40, 160, 120, 100)
                #pdf.cell(30,10, df.describe().loc[['mean']],0,0,'c')
                pdf.text(130, 270, 'Duration')
                pdf.text(160, 270, str(max(self.xAxis[0])))
                pdf.text(-52, 270, self.r.to_string())
                pdf.ln(10)
                pdf.text(-50, 290, self.p.to_string())

                pdf.output(str(pdname[0]))
               # TODO zabtahaaaaaaaa
                QtWidgets.QMessageBox.information(
                    self, 'Done', 'PDF has been created')
#------------------------------------------------------------------------------------------------------------------------------------------------------#


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
