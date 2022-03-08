from msilib.schema import Directory
from re import A
from tkinter import Label, dialog
from tkinter.tix import DirSelectDialog
from PyQt5 import QtWidgets, uic
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTextEdit, QFileDialog, QScrollBar, QComboBox, QColorDialog, QCheckBox, QSlider
from numpy.lib.index_tricks import IndexExpression

import pyqtgraph as pg
from pyqtgraph import PlotWidget
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
#from PDF import PDF
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

        interfacing.ChannelLineArr[interfacing.SignalSelectedIndex].Amplitude = TempArrY
        interfacing.ChannelLineArr[interfacing.SignalSelectedIndex].Time = TempArrX
        interfacing.ChannelLineArr[interfacing.SignalSelectedIndex].Filepath = path

        interfacing.initSpectroRangeSliders(self)
        self.plotSpectro()

        self.plot_data()  # starts plot after file is accessed

    def plot_data(self):
        self.x = self.time
        self.y = self.amplitude
        pen = pg.mkPen(color=(255, 255, 255))
        self.data_line = self.Plot.plot(self.x, self.y, pen=pen)
        self.timer = QtCore.QTimer()
        self.timer.setInterval(150)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

    # def InitDataPoints(self):

    def update_plot_data(self):
        self.x = self.x[1:]  # Remove the first y element.
        # Add a new value 1 higher than the last.
        self.x.append(self.x[-1] + 1)

        self.data_line.setData(
            self.x, self.y, pen=interfacing.ChannelLineArr[interfacing.SignalSelectedIndex].GetColour())

        for ChannelIndex in range(len(interfacing.ChannelLineArr)):
            # checks if signal has information to be plotted
            # Check if channel contains data (TODO: change this later to a bool)
            if interfacing.ChannelLineArr[ChannelIndex].Filepath != "null":

                # Index of channels containing files
                # self.FilledChannels.append(ChannelIndex)

                self.xAxis[ChannelIndex] = interfacing.ChannelLineArr[ChannelIndex].Time[:self.pointsToAppend]
                self.yAxis[ChannelIndex] = interfacing.ChannelLineArr[ChannelIndex].Amplitude[:self.pointsToAppend]

        self.pointsToAppend += 5

        # TODO: if the shortest signal ends stop the timer

        # DEBUGGING LOOP
        # for Index in range(3):
        #     if interfacing.ChannelLineArr[Index].Filepath != "null":
        #         interfacing.printDebug("Channel number: " + str(Index))
        #         interfacing.printDebug(
        #             len(interfacing.ChannelLineArr[Index].Time))
        #         interfacing.printDebug(len(self.xAxis[Index]))

        self.horizontalScrollBarFunction()
        self.verticalScrollBarFunction()
        #interfacing.printDebug("Minimum signal length: " + str(MinSignalLen))
        if self.pointsToAppend > self.MinSignalLen:
            self.timer.stop()

        # TODO: Set y limits based on all plottable signals

        # Plots all signals
        for Index in range(3):  # TODO: make this variable later.;
            if interfacing.ChannelLineArr[Index].Filepath != "null":
                # TODO: signal should be time indexed
                # self.PlotWidget.setData(
                # self.xAxis[0], self.yAxis[Index], pen=interfacing.ChannelLineArr[Index].GetColour(), skipFiniteCheck=True)
                self.LineReferenceArr[Index].setData(
                    self.xAxis[0], self.yAxis[Index], pen=interfacing.ChannelLineArr[Index].GetColour(), skipFiniteCheck=True)

#-----------------------------------------------------------------------------------------------------------------------------------------------#
    # def ExportPDF(self):

    #     if self.pointsToAppend == 0:
    #         QtWidgets.QMessageBox.warning(
    #             self, 'NO SIGNAL !!', 'You have to plot a signal first')
    #     else:
    #    #create a CSV file of the signal
    #         ex1 = pg.exporters.CSVExporter(self.Plot.plotItem)
    #         ex1.export('test.csv')
    #    #create a excell sheet of the signal
    #         ex2 = pg.exporters.SVGExporter(self.Plot.plotItem)
    #         ex2.export('test.svg')
    #    #create a picture of the signal
    #         ex3 = pg.exporters.ImageExporter(self.Plot.plotItem)
    #         ex3.export('test.png')

    #     self.list = ['test.png']
    #     self.create_pdf()

    # def create_pdf(self):
    #     #the function that creates the pdf report

    #     pdf = FPDF()

    #     for index in range(1):
    #         # set pdf title
    #         pdf.add_page()
    #         pdf.set_font('Arial', 'B', 15)
    #         pdf.cell(70)
    #         pdf.cell(60, 10, 'Siganl Viewer Report', 1, 0, 'C')

    #         pdf.ln(20)

    #         # put the graphs on the pdf
    #         pdf.image(self.list[index], 10, 50, 190, 50)
    #        # pdf.image(self.spectroImg_list[index], 10, 110, 190, 100)
    #         pdf.drawString(50,380,'Spectrogram:')
    #         pdf.drawImage('sp'+str+'.png', 120, 80, width = 380 , height = 288)

    #     pdf.output("report.pdf", "F")
    #     #pdf.export('pdf.pdf')

    #     # #removes the graphs pictures as we dont need
    #     os.remove("test.png")
    #     os.remove("test.csv")
    #     os.remove("test.svg")

        # os.remove("fileName2.png")
        # os.remove("fileName3.png")
        # os.remove("spectro1.png")
        # os.remove("spectro2.png")
        # os.remove("spectro3.png")

        # Folder Dialog (failed attempt)
        # QFileDialog.setFileMode(self, Directory)
        # QFileDialog.setOption(self, DirSelectDialog)
        # self.filename = QFileDialog.getOpenFileName()
        # interfacing.printDebug(self.filename)
        # @Abdullahsaeed etfaddal hena

        # Step 1 choose folder location
        # Step 2 create snapshot of plotter
        # Step 3 create report with required variables and formatting
        # Step 4 save in selected folder location (step 1)
#-----------------------------------------------------------------------------------------------------------------------------------------------#


#-----------------------------------------------------------------------------------------------------------------------------------------------#
    # OPENS COLOUR DIALOG WHEN BUTTON IS PRESSED

    def DynamicUpdate(self):
        for Index in range(3):  # TODO: make this variable later
            if interfacing.ChannelLineArr[Index].Filepath != "null":
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
        self.timer.stop()     #Stopping the signal in order to view a specific point
        self.PauseToggleVar = True               #setting the toggle to true in order to press play to continue plotting 
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

    def horizontalScrollBarFunction(self):

        self.ValueHorizontal = self.horizontalScrollBar.value()

        if self.HoldVarH == True:  # law al value bata3 al scroll at8yar dah ma3nah ano 3aiz maymshesh ma3a al line
            self.Plot.plotItem.setXRange(
                interfacing.ChannelLineArr[0].Time[self.ValueHorizontal]-1.0, interfacing.ChannelLineArr[0].Time[self.ValueHorizontal])
        else:
            self.Plot.plotItem.setXRange(
                max(self.xAxis[0], default=0)-1.0, max(self.xAxis[0], default=0))
            self.ValueHorizontal = self.horizontalScrollBar.setValue(
                max(self.xAxis[0], default=0)*2000)

        self.horizontalScrollBar.setMinimum(0)
        self.horizontalScrollBar.setMaximum(
            len(interfacing.ChannelLineArr[0].Time))
        self.horizontalScrollBar.setSingleStep(20)

        interfacing.printDebug("Horizontal Scroll: " +
                               str(self.ValueHorizontal))

    def IsHeldH(self):
        self.HoldVarH = True  # mamsoka

    def NotHeldH(self):
        self.HoldVarH = False  # etsabet

    def IsHeldV(self):
        self.HoldVarV = True  # mamsoka

    def NotHeldV(self):
        self.HoldVarV = False  # etsabet

    def verticalScrollBarFunction(self):
        self.ValueVertical = self.verticalScrollBar.value()
         
        self.verticalScrollBar.setMinimum(0)
        self.verticalScrollBar.setMaximum(len(interfacing.ChannelLineArr[0].Amplitude))
        self.verticalScrollBar.setSingleStep(20)
         # TODO: after Setting limits based on all plottable signals
         #we will have the max and min of y axis 
         #by subtracting them we get the length of y axis 
         MaxY
         MinY 
         MyRange=(MaxY-MinY)/5
        if self.HoldVarV == True:  #law al value bata3 al scroll at8yar dah ma3nah ano 3aiz maymshesh ma3a al line  
            if self.ValueVertical>=0 and self.ValueVertical<=(len(interfacing.ChannelLineArr[0].Amplitude)*(1/5): #len(interfacing.ChannelLineArr[0].Amplitude) will be replaced with number of points on the plot 
                                                                      #in order to get the max number of values
                self.Plot.plotItem.setYRange(MaxY-MyRange,MaxY) #TAKECARE:hasabat al range hena (n)
            elif self.ValueVertical>=(len(interfacing.ChannelLineArr[0].Amplitude)*(1/5) and self.ValueVertical<=(len(interfacing.ChannelLineArr[0].Amplitude)*(2/5):    
                                                                                                                  
                self.Plot.plotItem.setYRange(Max-MyRange*2,Max-MyRange)

            elif self.ValueVertical>=(len(interfacing.ChannelLineArr[0].Amplitude)*(2/5) and self.ValueVertical<=(len(interfacing.ChannelLineArr[0].Amplitude)*(3/5)
                self.Plot.plotItem.setYRange(Max-MyRange*3,Max-MyRange*2)
 
            elif self.ValueVertical>=(len(interfacing.ChannelLineArr[0].Amplitude)*(3/5) and self.ValueVertical<=(len(interfacing.ChannelLineArr[0].Amplitude)*(4/5)
                self.Plot.plotItem.setYRange(Max-MyRange*4,Max-MyRange*3)
            else:
                self.Plot.plotItem.setYRange(MinY,Max-MyRange*4)


        else:
            self.Plot.plotItem.setYRange(min(self.yAxis[0], default=0), max(self.yAxis[0], default=0)) # we might need to make the range const
            self.ValueVertical = self.verticalScrollBar.setValue(0)  #at amplitude=0


            
        
       
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
#--------------------------------------------------------------- Table FUNCTIONS ---------------------------------------------------------------------------------------------------#

    def createTable(self):
        self.tableWidget = QTableWidget()

        # Row count
        self.tableWidget.setRowCount(4)

        # Column count
        self.tableWidget.setColumnCount(2)

        self.tableWidget.setItem(0, 0, QTableWidgetItem(min))
        self.tableWidget.setItem(0, 1, QTableWidgetItem(max))
        self.tableWidget.setItem(1, 0, QTableWidgetItem("Aloysius"))
        self.tableWidget.setItem(1, 1, QTableWidgetItem("Indore"))
        self.tableWidget.setItem(2, 0, QTableWidgetItem("Alan"))
        self.tableWidget.setItem(2, 1, QTableWidgetItem("Bhopal"))
        self.tableWidget.setItem(3, 0, QTableWidgetItem("Arnavi"))
        self.tableWidget.setItem(3, 1, QTableWidgetItem("Mandsaur"))

#--------------------------------------------------------------- EXPORT FUNCTIONS --------------------------------------------------------------------------------------------------#

    def ExportPDF(self):

        # TODO make the messages valid
        if self.pointsToAppend == 0:
            QtWidgets.QMessageBox.warning(
                self, 'NO SIGNAL ', 'You have to plot a signal first')
        elif self.pointsToAppend != 0:
            QtWidgets.QMessageBox.information(
                self, 'Done', 'PDF has been created')
       # create a CSV file of the signal
            ex1 = pg.exporters.CSVExporter(self.Plot.plotItem)
            ex1.export('test.csv')
       # create a excell sheet of the signal
            ex2 = pg.exporters.SVGExporter(self.Plot.plotItem)
            ex2.export('test.svg')
       # create a picture of the signal
            ex3 = pg.exporters.ImageExporter(self.Plot.plotItem)
            ex3.export('test.png')
       # put the picture of the signal in an array
        self.list = ['test.png']
        # call the function create_pdf()

        self.create_pdf()

#--------------------------------------------------------------------------------CREATE TABLE------------------------------------------------------------#

    def createTable(self):
        self.tableWidget = QTableWidget()

        # Row count
        self.tableWidget.setRowCount(4)

        # Column count
        self.tableWidget.setColumnCount(2)

        self.tableWidget.setItem(0, 0, QTableWidgetItem("Name"))
        self.tableWidget.setItem(0, 1, QTableWidgetItem("City"))
        self.tableWidget.setItem(1, 0, QTableWidgetItem("Aloysius"))
        self.tableWidget.setItem(1, 1, QTableWidgetItem("Indore"))
        self.tableWidget.setItem(2, 0, QTableWidgetItem("Alan"))
        self.tableWidget.setItem(2, 1, QTableWidgetItem("Bhopal"))
        self.tableWidget.setItem(3, 0, QTableWidgetItem("Arnavi"))
        self.tableWidget.setItem(3, 1, QTableWidgetItem("Mandsaur"))

        self.create_pdf()
  #-----------------------------------------------------------------------------------------------------------------------------------#

    def create_pdf(self):
        # the function that creates the pdf report
        pdname = QFileDialog.getSaveFileUrl(
            None, str('Save the signal file'), None, str("PDF FIles(*.pdf)"))
        print(self.pdname[0])

        if pdname != '':
            pdf = FPDF()
            # set pdf title
            pdf.add_page()
            pdf.set_font('Arial', 'B', 15)
            pdf.cell(70)
            pdf.cell(60, 10, 'Signal Viewer Report', 1, 0, 'C')
            pdf.ln(5)
           # pdf.cell(60, 10, 'Abdullah', 0, 0, 'L')

            pdf.ln(20)

            # put the graphs on the pdf
            pdf.image('Desgin/CUFE.png', 1, 1, 50, 40)
            pdf.image('Desgin/logo.png', 160, 1, 50, 40)

            pdf.image('test.png', 40, 50, 100, 100)
            pdf.image('Spectrogram.png', 40, 160, 100, 100)
            pdf.output(str(pdname[0]))
            # pdf.image()

        # path = self.filename

        # removes the graphs pictures as we dont need
        os.remove("test.png")
        os.remove("test.csv")
        os.remove("test.svg")
        os.remove('Spectrogram.png')


#------------------------------------------------------------------------------------------------------------------------------------------------------#

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


# BASIC CODE TO TEST WHETHER PYQTGRAPH WIDGET LOADS
