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

        # self.amplitude = []
        # self.time = []
        # self.filename = ['']
        self.xAxis = []
        self.yAxis = []
        self.pointsToAppend = 0

    def Browse(self):
        self.filename = QFileDialog.getOpenFileName(
            None, 'open the signal file', './', filter="Raw Data(*.csv *.txt *.xls)")
        path = self.filename[0]
        interfacing.printDebug("Selected path: " + path)
        self.OpenFile(path)

    def OpenFile(self, path: str):
        with open(path, 'r') as csvFile:    # 'r' its a mode for reading and writing
            csvReader = csv.reader(csvFile, delimiter=',')
            for line in csvReader:
                interfacing.ChannelLineArr[interfacing.SignalSelectedIndex].Amplitude.append(
                    float(line[1]))
                interfacing.ChannelLineArr[interfacing.SignalSelectedIndex].Time.append(
                    float(line[0]))
        self.plot_data()  # starts plot after file is accessed

    def plot_data(self):
        # TODO: Initialize Plotter Array
        self.PlotterLineArr = []

        # TODO: Make this range dependent on max current channels variable
        for LineIndex in range(3):
            pen = pg.mkPen(color=(255, 255, 255))
            self.PlotterLineArr.append(self.Plot.plot(pen=pen))

        # self.Plot.plotItem.setLimits(xMin=min(self.time), xMax=max(self.time), yMin=min(
        #     self.amplitude), yMax=max(self.amplitude))  # limit bata3 al axis ali 3andi
        self.pointsToAppend = 0  # Plotted Points counter

        # Initialize Qt Timer
        self.timer = QtCore.QTimer()
        self.timer.setInterval(20)  # Overflow timer
        self.timer.timeout.connect(self.update_plot_data)  # Event handler
        self.timer.start()  # Start timer

    # def InitDataPoints(self):

    def update_plot_data(self):

        for ChannelIndex in range(len(interfacing.ChannelLineArr)):
            # checks if signal has information to be plotted
            # Check if channel contains data (TODO: change this later to a bool)
            if interfacing.ChannelLineArr[ChannelIndex].Filepath != "null":

                # Index of channels containing files
                self.FilledChannels.append(ChannelIndex)

                self.xAxis[ChannelIndex] = interfacing.ChannelLineArr[ChannelIndex].Amplitude[:self.pointsToAppend]
                self.yAxis[ChannelIndex] = interfacing.ChannelLineArr[ChannelIndex].Time[:self.pointsToAppend]
        interfacing.printDebug(self.xAxis[0])
        self.pointsToAppend += 10
        # if self.pointsToAppend > len(self.time):
        #     self.timer.stop()
        # TODO: if the shortest signal ends stop the timer
        #MinSignalLen = min(map(len, interfacing.ChannelLineArr.Time))
        MinSignalLen = 10000000
        #interfacing.printDebug("Minimum signal length: " + str(MinSignalLen))
        if self.pointsToAppend > MinSignalLen:
            self.timer.stop()

        # if self.time[self.pointsToAppend] > 1:   #1 because this where our axis stops at at the begings to evry time we need to update the axis inorder for it to plot dynamiclly
        # self.Plot.setLimits(xMax=max(self.x, default=0))

        # TODO: Create array of dataline objects and update each one according to its appended values
        # TODO: Set y limits based on all plottable signals
        # TODO: Zoom and scrolling might require changes to limits

        # TODO: to be embedded as in the class plotwindow
        # VisibleYRange = (0,0)
        # VisibleXRange = (0,0)

        # self.Plot.plotItem.setXRange(
        #     max(self.x, default=0)-1.0, max(self.x, default=0))

        for Index in range(len(self.PlotterLineArr)):
            if interfacing.ChannelLineArr[Index].Filepath != "null":
                
                self.PlotterLineArr[Index].setData(
                    self.xAxis[Index], self.yAxis[Index], pen=interfacing.ChannelLineArr[Index].GetColour(), skipFiniteCheck=True)

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
        interfacing.printDebug("Pause")


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


# BASIC CODE TO TEST WHETHER PYQTGRAPH WIDGET LOADS
