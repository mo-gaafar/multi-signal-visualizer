from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTextEdit, QFileDialog, QScrollBar, QComboBox, QColorDialog, QCheckBox, QSlider
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5 import QtWidgets, uic
from fpdf import FPDF
import pyqtgraph.exporters
import pyqtgraph as pg
import pandas as pd
import statistics
import os

# the function that creates the pdf report


def Exporter(self):
        if self.pointsToAppend == 0:
            QtWidgets.QMessageBox.warning(
                self, 'NO SIGNAL ', 'You have to plot a signal first')
        else:
            FolderPath = QFileDialog.getSaveFileName(
                None, str('Save the signal file'), None, str("PDF FIles(*.pdf)"))
            if FolderPath != '':
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
                ex1.export('temp.csv')

                df = pd.read_csv('temp.csv')
                self.r = df.describe().loc[['mean', 'min']]
                self.p = df.describe().loc[['max', 'std']]

                self.E = df.describe()
            #   print(self.E)
                # pdf.cell(50, 10, self.E, 0, 0, 'C')

        # create an SVG of the signal

                ex2 = pg.exporters.SVGExporter(self.Plot.plotItem)
                ex2.export('temp.svg')
        # create a picture of the signal
                ex3 = pg.exporters.ImageExporter(self.Plot.plotItem)
                ex3.export('temp.png')
        # put the picture of the signal in an array
                self.list = ['temp.png']
        # call the function create_pdf()
                # put the graphs on the pdf
                pdf.image('Desgin/CUFE.png', 1, 1, 50, 40)
                pdf.image('Desgin/logo.png', 160, 1, 50, 40)
                pdf.image('temp.png', 40, 50, 150, 100)
                pdf.image('Spectrogram.png', 40, 160, 120, 100)
                # pdf.cell(30,10, df.describe().loc[['mean']],0,0,'c')
                pdf.text(130, 270, 'Duration')
                pdf.text(160, 270, str(max(self.xAxis[0])))
                pdf.text(-52, 270, self.r.to_string())
                pdf.ln(10)
                pdf.text(-50, 290, self.p.to_string())

                pdf.output(str(FolderPath[0]))

                QtWidgets.QMessageBox.information(
                    self, 'Done', 'PDF has been created')

                # deletes temporary files
                os.remove("temp.csv")
                os.remove("temp.png")
                os.remove("temp.svg")
                os.remove("Spectrogram.png")
