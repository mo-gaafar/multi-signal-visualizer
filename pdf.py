from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTextEdit, QFileDialog, QScrollBar, QComboBox, QColorDialog, QCheckBox, QSlider
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5 import QtWidgets, uic
from fpdf import FPDF
import pyqtgraph.exporters
import pyqtgraph as pg
import pandas as pd
import statistics
import os
import numpy as np
# the function that creates the pdf report


def Exporter(self):
    if self.pointsToAppend == 0:
        # This message appears if there is no signal to EXPORT
        QtWidgets.QMessageBox.warning(
            self, 'NO SIGNAL ', 'You have to plot a signal first')
    else:
        FolderPath = QFileDialog.getSaveFileName(
            None, str('Save the signal file'), None, str("PDF FIles(*.pdf)"))
        if FolderPath != '':
            pdf = FPDF()

            # Add new page. Without this you cannot create the document
            pdf.add_page()

            # Style of the pdf
            # pdf.set_font('ZapfDingbats','B',20)
            pdf.set_font('Arial', 'B', 20)
            pdf.cell(70)
            pdf.cell(50, 10, 'Signal Viewer Report', 0, 0, 'C')

            # create a picture of the signal
            ex3 = pg.exporters.ImageExporter(self.Plot.plotItem)
            ex3.export('plot.png')

            # insert the logos
            pdf.image('Desgin/CUFE.png', 1, 1, 50, 40)
            pdf.image('Desgin/logo.png', 160, 1, 50, 40)

            # insert the plot graph and the specrogram
            pdf.image('plot.png', 40, 50, 150, 100)
            pdf.image('Spectrogram.png', 55, 160, 120, 100)

            # Adding new page for the table
            pdf.add_page()

            pdf.set_font('Times', '', 10.0)

            # Effective page width, or just epw
            epw = pdf.w - 2*pdf.l_margin

            # distribute the table on 6 columes
            column_width = epw/6

            # declare an array of the arrays.  Also we declared the size
            data = [['', 'Max', 'Min', 'Mean', 'Std_Dev', 'Duration'], [], [], []]

            # This loop to draw the rest of the rows and to get the varibles to fill the table
            for index in range(3):
                if self.ChannelLineArr[index].Filepath != "null":
                    data[index+1].append('Channel ' + str(index + 1))
                    data[index +
                         1].append(round(np.amax(self.ChannelLineArr[index].Amplitude), 4))
                    data[index +
                         1].append(round(np.amin(self.ChannelLineArr[index].Amplitude), 4))
                    data[index +
                         1].append(round(np.mean(self.ChannelLineArr[index].Amplitude), 4))
                    data[index +
                         1].append(round(np.std(self.ChannelLineArr[index].Amplitude), 4))
                    data[index +
                         1].append(round(np.amax(self.ChannelLineArr[index].Time), 4))

            # Document title centered, 'B'old, 14 pt
            pdf.set_font('Times', 'B', 20.0)
            pdf.cell(epw, 0.0, 'Statistics data', align='C')
            pdf.set_font('Times', '', 10.0)
            pdf.ln(20)

            # Text height is the same as current font size
            text_height = pdf.font_size

            # This 2 loops draw the Table
            for row in data:
                for datum in row:

                    # This condition to select the first column
                    if datum == row[0]:
                        # Set the color of the first column
                        pdf.set_fill_color(200, 200, 200)
                        # Draw the first column
                        pdf.cell(column_width, 3*text_height,
                                 str(datum), border=1, fill=True)

                    # This condition to select the first row
                    elif row == data[0]:
                        # Set the color of the first row
                        pdf.set_fill_color(200, 200, 200)
                        # Draw the first row
                        pdf.cell(column_width, 3*text_height,
                                 str(datum), border=1, fill=True)
                    else:
                        pdf.cell(column_width, 3*text_height,
                                 str(datum), border=1)

            # Line break equivalent to 3 lines
                pdf.ln(3*text_height)

            # Exporting the Pdf
            pdf.output(str(FolderPath[0]))

        # This message appears when the pdf EXPORTED
            QtWidgets.QMessageBox.information(
                self, 'Done', 'PDF has been created')

            os.remove("plot.png")
            os.remove("Spectrogram.png")

    #  pdf.SetAutoPageBreak(boolean auto [, float margin])
