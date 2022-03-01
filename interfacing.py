from PyQt5 import QtWidgets, uic
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTextEdit, QFileDialog, QScrollBar, QComboBox

from pyqtgraph import PlotWidget
import pyqtgraph as pg
import sys

# Initializes all event triggers


def initConnectors(self):

    # Browse button
    self.BrowseButton = self.findChild(QPushButton, "BrowseButton")
    self.BrowseButton.clicked.connect(self.Browse)

    self.ExportBtn = self.findChild(QPushButton, "ExportBtn")
    self.ExportBtn.clicked.connect(self.Browse)
