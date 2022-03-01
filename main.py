from msilib.schema import Directory
from tkinter import Label, dialog
from tkinter.tix import DirSelectDialog
from PyQt5 import QtWidgets, uic
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTextEdit, QFileDialog, QScrollBar, QComboBox

from pyqtgraph import PlotWidget
import pyqtgraph as pg
import sys

import interfacing  # local module


class MainWindow(QtWidgets.QMainWindow):

    # Initialization function
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('mainwindow2.ui', self)

        interfacing.initConnectors(self)

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

    def ZoomInFunction(self):
        null = null

    def ZoomOutFunction(self):
        null = null

    def TogglePause(self):
        null = null

    def UpdateLineProperty(self):
        # print(interfacing.ChannelProperties
        null = null
        # Line Colour
        self.NewLabel = interfacing.ChannelPropertiesArr[interfacing.CurrentChannelProperty].LineColour
        # Insert Function to set line colour
        # Visibility (IsHidden?)
        self.IsHidden = interfacing.ChannelPropertiesArr[interfacing.CurrentChannelProperty].IsHidden
        # Insert Function to set line visibility
        # Label
        self.NewLabel = interfacing.ChannelPropertiesArr[interfacing.CurrentChannelProperty].Label
        # Insert function to set label

    def UpdateSpectrogramProperty(self):
        null = null  # placeholder


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


# BASIC CODE TO TEST WHETHER PYQTGRAPH WIDGET LOADS
