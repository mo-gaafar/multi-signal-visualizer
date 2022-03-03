from msilib.schema import Directory
from tkinter import Label, dialog
from tkinter.tix import DirSelectDialog
from PyQt5 import QtWidgets, uic
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTextEdit, QFileDialog, QScrollBar, QComboBox, QColorDialog

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

        self.amplitude = []
        self.time = []
        self.filename = ['']
        self.pointsToAppend= 0

    def openfile(self, path: str):  # to read the content of the
        with open(path, 'r') as csvFile:    # 'r' its a mode for reading and writing
            csvReader = csv.reader(csvFile, delimiter=',')
            for line in csvReader:
                self.amplitude.append(float(line[1]))
                self.time.append(float(line[0]))
        self.plot_data()


    def plot_data(self):
        pen = pg.mkPen(color=(255, 255, 255))
        self.data_line = self.Plot.plot(self.time, self.amplitude, pen=pen)
        print('PASS1')
        self.Plot.plotItem.setLimits(xMin=min(self.time), xMax=max(self.time), yMin=min(self.amplitude), yMax=max(self.amplitude)) #limit bata3 al axis ali 3andi
        print('PASS2')
        
        self.pointsToAppend= 0
        self.timer = QtCore.QTimer()
        self.timer.setInterval(20)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()
        print('PASS3')

    def update_plot_data(self):

        self.x = self.time[:self.pointsToAppend]
        self.y = self.amplitude[:self.pointsToAppend]
        self.pointsToAppend += 10
        if self.pointsToAppend > len(self.time):
            self.timers.stop()
            
        print(self.pointsToAppend)
        print(len(self.time))
        print(self.time[self.pointsToAppend])
        print('nultgfuktgcukl')
        print(self.time[:self.pointsToAppend])

        print('PASS4')
        #if self.time[self.pointsToAppend] > 1:   #1 because this where our axis stops at at the begings to evry time we need to update the axis inorder for it to plot dynamiclly
           # self.Plot.setLimits(xMax=max(self.x, default=0))
        print('PASS5')
        self.Plot.plotItem.setXRange(max(self.x, default=0)-1.0, max(self.x, default=0))
        print('PASS6')
        self.data_line.setData(self.x, self.y, pen=interfacing.ChannelLineArr[interfacing.SignalSelectedIndex].GetColour())

    def Browse(self):
        self.filename = QFileDialog.getOpenFileName(
            None, 'open the signal file', './', filter="Raw Data(*.csv *.txt *.xls)")
        path = self.filename[0]
        print("Selected path: " + path)
        self.openfile(path)

    def ExportPDF(self):
        # Folder Dialog (failed attempt)
        QFileDialog.setFileMode(self, Directory)
        QFileDialog.setOption(self, DirSelectDialog)
        self.filename = QFileDialog.getOpenFileName()
        print(self.filename)
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
        if DebugMode == True:
            interfacing.printbtengan()

    def ZoomOutFunction(self):
        if DebugMode == True:
            interfacing.printbtengan()

    def TogglePause(self):
        if DebugMode == True:
            interfacing.printbtengan()

    def UpdateLineProperty(self):
        if DebugMode == True:
            interfacing.printbtengan()
        # Line Colour
        self.NewLabel = interfacing.ChannelLineArr[interfacing.SignalSelectedIndex].LineColour
        # Insert Function to set line colour
        # Visibility (IsHidden?)
        self.IsHidden = interfacing.ChannelLineArr[interfacing.SignalSelectedIndex].IsHidden
        # Insert Function to set line visibility
        # Label
        self.NewLabel = interfacing.ChannelLineArr[interfacing.SignalSelectedIndex].Label
        # Insert function to set label

    def UpdateSpectrogramProperty(self):
        if DebugMode == True:
            interfacing.printbtengan()


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


# BASIC CODE TO TEST WHETHER PYQTGRAPH WIDGET LOADS
