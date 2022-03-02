from msilib.schema import Directory
from tkinter import Label, dialog
from tkinter.tix import DirSelectDialog
from PyQt5 import QtWidgets, uic
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTextEdit, QFileDialog, QScrollBar, QComboBox, QColorDialog

from pyqtgraph import PlotWidget
import pyqtgraph as pg
import sys

import os
from random import randint

import interfacing  # local module

DebugMode = True #Debug mode enables printing


class MainWindow(QtWidgets.QMainWindow):

    # Mainwindow constructor
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('mainwindow2.ui', self)

        #Initialization functions
        interfacing.initConnectors(self)
        interfacing.initArrays(self)

#------------------------------------------------------------------------------------------------------------------------------------------------------------
        self.x = list(range(100))  # 100 time points
        self.y = [randint(0,100) for _ in range(100)]
        pen = pg.mkPen(color=(255, 255, 255))
        self.data_line =  self.Plot.plot(self.x, self.y, pen=pen)
        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()
                                                                                    # RANDOM REAL TIME EXAMPLE
    def update_plot_data(self):
        self.x = self.x[1:]  # Remove the first y element.
        self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.

        self.y = self.y[1:]  # Remove the first
        self.y.append(randint(-100,100))  # Add a new random value.

        self.data_line.setData(self.x, self.y)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------

       

    def Browse(self):
        self.filename = QFileDialog.getOpenFileName()
        print(self.filename)

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

    def SelectSignalColour(self):                               # OPENS COLOUR DIALOG WHEN BUTTON IS PRESSED
        self.SignalColour = QColorDialog.getColor()
        print(self.SignalColour)

    def ZoomInFunction(self):
        interfacing.printbtengan()

    def ZoomOutFunction(self):
        interfacing.printbtengan()

    def TogglePause(self):
        interfacing.printbtengan()

    def UpdateLineProperty(self):
        # print(interfacing.ChannelProperties
        null = null
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
        interfacing.printbtengan()  # placeholder


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


# BASIC CODE TO TEST WHETHER PYQTGRAPH WIDGET LOADS
