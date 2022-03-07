from msilib.schema import Directory
from tkinter import Label, dialog
from tkinter.tix import DirSelectDialog
from PyQt5 import QtWidgets, uic
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTextEdit, QFileDialog, QScrollBar, QComboBox, QColorDialog, QCheckBox
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

import interfacing  # local module



DebugMode = True  # Debug mode enables printing



class MainWindow(QtWidgets.QMainWindow):

    # Mainwindow constructor
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('mainwindow2.ui', self)

        # Initialization functions
        interfacing.initConnectors(self)
        interfacing.initArrays(self)
        interfacing.CreateSpectrogramFigure(self)

        self.PlotterWindowProp = interfacing.PlotterWindow()
        self.PauseToggleVar = False
        self.HoldVarH = False
        self.HoldVarV = False
        self.xAxis = [0,0,0]
        self.yAxis = [0,0,0]
        
        self.LineReferenceArr = [self.Plot.plot(self.xAxis,self.yAxis), self.Plot.plot(self.xAxis,self.yAxis), self.Plot.plot(self.xAxis, self.yAxis)]



    def Browse(self):
        self.filename = QFileDialog.getOpenFileName(
            None, 'open the signal file', './', filter="Raw Data(*.csv *.txt *.xls)")
        path = self.filename[0]
        interfacing.printDebug("Selected path: " + path)
        self.OpenFile(path)

    def OpenFile(self, path: str):
        TempArrX = []
        TempArrY = []

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


        self.plot_data()  # starts plot after file is accessed

    def plot_data(self):

        pen = pg.mkPen(color=(255, 255, 255))
        self.PlotWidget = self.Plot.plot(pen= pen)
        self.Plot.showGrid(x = True, y = True)
        self.Plot.addLegend()

        self.MinSignalLen = len(interfacing.ChannelLineArr[0].Amplitude)
        interfacing.printDebug("Max length of x plots is: " + str(self.MinSignalLen))
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
        #self.Plot.plotItem.setLimits(xMin=min(self.time), xMax=max(self.time), yMin=min(
        #     self.amplitude), yMax=max(self.amplitude))  # limit bata3 al axis ali 3andi
        MinY = -1 #Placeholder
        interfacing.printDebug("MaxX: " + str(MaxX))
        self.Plot.plotItem.setLimits(xMin=0, xMax=MaxX, yMin=MinY, yMax=MaxY)  # limit bata3 al axis ali 3andi
        self.pointsToAppend = 0  # Plotted Points counter 

         # Initialize Qt Timer
        self.timer = QtCore.QTimer()
        self.timer.setInterval(150)  # Overflow timer
        self.timer.timeout.connect(self.update_plot_data)  # Event handler
        self.timer.start()  # Start timer

        
       
          
    # def InitDataPoints(self):

    def update_plot_data(self):

        self.timer.setInterval(100*self.PlotterWindowProp.CineSpeed)

        for ChannelIndex in range(len(interfacing.ChannelLineArr)):
            # checks if signal has information to be plotted
            # Check if channel contains data (TODO: change this later to a bool)
            if interfacing.ChannelLineArr[ChannelIndex].Filepath != "null":
                
                # Index of channels containing files
                #self.FilledChannels.append(ChannelIndex)

                self.xAxis[ChannelIndex] = interfacing.ChannelLineArr[ChannelIndex].Time[:self.pointsToAppend]
                self.yAxis[ChannelIndex] = interfacing.ChannelLineArr[ChannelIndex].Amplitude[:self.pointsToAppend]

        #interfacing.printDebug(self.xAxis[0])
        self.pointsToAppend += 5
        # if self.pointsToAppend > len(self.time):
        #     self.timer.stop()
        # TODO: if the shortest signal ends stop the timer
        #MinSignalLen = min(map(len, interfacing.ChannelLineArr.Time))

        #DEBUGGING LOOP
        for Index in range(3):
            if interfacing.ChannelLineArr[Index].Filepath != "null":
                interfacing.printDebug("Channel number: " + str(Index))
                interfacing.printDebug(len(interfacing.ChannelLineArr[Index].Time))
                interfacing.printDebug(len(self.xAxis[Index]))
        self.horizontalScrollBarFunction()
        self.verticalScrollBarFunction()
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
      
       
            

        #TODO: fix this 
     
       
        #Plots all signals
        for Index in range(3): #TODO: make this variable later.;
            if interfacing.ChannelLineArr[Index].Filepath != "null":
                #TODO: signal should be time indexed
                #self.PlotWidget.setData(
                    #self.xAxis[0], self.yAxis[Index], pen=interfacing.ChannelLineArr[Index].GetColour(), skipFiniteCheck=True)
                self.LineReferenceArr[Index].setData(self.xAxis[0], self.yAxis[Index], pen=interfacing.ChannelLineArr[Index].GetColour(), skipFiniteCheck=True)
                
          


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
        self.Plot.plotItem.getViewBox().scaleBy((0.5, 0.5))
        interfacing.printDebug("Zoomin")

    def ZoomOutFunction(self):
        self.Plot.plotItem.getViewBox().scaleBy((1.5, 1.5))
        interfacing.printDebug("Zoomout")

    def TogglePause(self):
        self.PauseToggleVar = not self.PauseToggleVar #On click, toggle state
        if self.PauseToggleVar == True:
            self.timer.stop()
        else:
            self.timer.start()
        interfacing.printDebug("PauseToggle")

    def horizontalScrollBarFunction(self):
        
        self.ValueHorizontal = self.horizontalScrollBar.value()

        if self.HoldVarH == True:  #law al value bata3 al scroll at8yar dah ma3nah ano 3aiz maymshesh ma3a al line  
            self.Plot.plotItem.setXRange(interfacing.ChannelLineArr[0].Time[self.ValueHorizontal]-1.0,interfacing.ChannelLineArr[0].Time[self.ValueHorizontal])
        else:
            self.Plot.plotItem.setXRange(max(self.xAxis[0], default=0)-1.0, max(self.xAxis[0], default=0))
            self.ValueHorizontal = self.horizontalScrollBar.setValue(max(self.xAxis[0], default=0)*2000)


            
        
        self.horizontalScrollBar.setMinimum(0)
        self.horizontalScrollBar.setMaximum(len(interfacing.ChannelLineArr[0].Time))
        self.horizontalScrollBar.setSingleStep(20)
        
         
        interfacing.printDebug("Horizontal Scroll: " + str(self.ValueHorizontal))

    def IsHeldH (self):
        self.HoldVarH = True  #mamsoka

    def NotHeldH(self):
        self.HoldVarH = False #atsabat

    def IsHeldV (self):
        self.HoldVarV = True  #mamsoka 

    def NotHeldV(self):
        self.HoldVarV = False #atsabat


    def verticalScrollBarFunction(self):
        self.ValueVertical = self.verticalScrollBar.value()
         
        

        if self.HoldVarV == True:  #law al value bata3 al scroll at8yar dah ma3nah ano 3aiz maymshesh ma3a al line  
            if self.ValueVertical<(len(interfacing.ChannelLineArr[0].Amplitude)/2.0): #tala3 fo2

                self.Plot.plotItem.setYRange(min(interfacing.ChannelLineArr[0].Amplitude[:self.ValueVertical], default=0)+0.1,max(interfacing.ChannelLineArr[0].Amplitude[:self.ValueVertical], default=0)) #TAKECARE:hasabat al range hena (n)
            else:                                                                       #nazal ta7t
                self.Plot.plotItem.setYRange(min(interfacing.ChannelLineArr[0].Amplitude[:self.ValueVertical], default=0),max(interfacing.ChannelLineArr[0].Amplitude[:self.ValueVertical], default=0)-0.1)

        else:
            self.Plot.plotItem.setYRange(min(self.yAxis[0], default=0), max(self.yAxis[0], default=0)) #TAKECARE:hasabat al range hena
            self.ValueVertical = self.verticalScrollBar.setValue(len(interfacing.ChannelLineArr[0].Amplitude)/2.0)  #at amplitude=0


            
        
        self.verticalScrollBar.setMinimum(0)
        self.verticalScrollBar.setMaximum(len(interfacing.ChannelLineArr[0].Amplitude))
        self.verticalScrollBar.setSingleStep(20)
        interfacing.printDebug("Vertical Scroll: " + str(self.ValueVertical))
    
    def SpeedSliderFunction(self,Input):
        self.ValueCineSpeed = Input
        interfacing.printDebug("Speed Slider: " + str(self.ValueCineSpeed))
        self.PlotterWindowProp.UpdateCineSpeed(Input)
        return self.ValueCineSpeed

    def SpectrogramFrequency(self,Input, MinOrMax):
        if MinOrMax == "min":
            self.SpectroMinFrequency = Input
        if MinOrMax == "max":
            self.SpectroMaxFrequency = Input

        interfacing.printDebug(MinOrMax + "SpectroSlider: " + str(Input))


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


# BASIC CODE TO TEST WHETHER PYQTGRAPH WIDGET LOADS
