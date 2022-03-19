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


        # def Exporter(self):
        # if self.pointsToAppend == 0:
        #     QtWidgets.QMessageBox.warning(
        #         self, 'NO SIGNAL ', 'You have to plot a signal first')
        # else:
        #     FolderPath = QFileDialog.getSaveFileName(
        #         None, str('Save the signal file'), None, str("PDF FIles(*.pdf)"))
        #     if FolderPath != '':
        #         pdf = FPDF()
        #         # set pdf title
        #         pdf.add_page()
        #         pdf.set_font('Arial', 'B', 17)
        #         pdf.cell(70)

        #         pdf.cell(50, 10, 'Signal Viewer Report', 0, 0, 'C')
        #         pdf.ln(5)
        #     # pdf.cell(60, 10, 'Abdullah', 0, 0, 'L')

        #         pdf.ln(20)
        #     # create a CSV file of the signal
        #         ex1 = pg.exporters.CSVExporter(self.Plot.plotItem)
        #         ex1.export('temp.csv')

        #         df = pd.read_csv('temp.csv')
            
        #         self.r = df.describe().loc[['mean', 'min']]
        #         self.p = df.describe().loc[['max', 'std']]

        #         self.E = df.describe()
        #     #   print(self.E)
        #         # pdf.cell(50, 10, self.E, 0, 0, 'C')

        # # create an SVG of the signal

        #         ex2 = pg.exporters.SVGExporter(self.Plot.plotItem)
        #         ex2.export('temp.svg')
        # # create a picture of the signal
        #         ex3 = pg.exporters.ImageExporter(self.Plot.plotItem)
        #         ex3.export('temp.png')
        # # put the picture of the signal in an array
        #         self.list = ['temSp.png']
        # # call the function create_pdf()
        #         # put the graphs on the pdf
        #         pdf.image('Desgin/CUFE.png', 1, 1, 50, 40)
        #         pdf.image('Desgin/logo.png', 160, 1, 50, 40)
        #         pdf.image('temp.png', 40, 50, 150, 100)
        #         pdf.image('Spectrogram.png', 55, 270, 120, 100)
        #         # pdf.cell(30,10, df.describe().loc[['mean']],0,0,'c')
        #         pdf.add_page()
        #         pdf.text(130, 270, 'Duration')
        #         pdf.text(160, 270, str(max(self.xAxis[0])))
        #         pdf.text(-52, 270, self.r.to_string())
        #         pdf.ln(10)
        #         pdf.text(-50, 290, self.p.to_string())
            
        #         pdf.output(str(FolderPath[0]))

        #         QtWidgets.QMessageBox.information(
        #             self, 'Done', 'PDF has been created')

        #         # deletes temporary files
        #         os.remove("temp.csv")
        #         os.remove("temp.png")
        #         os.remove("temp.svg")
        #         os.remove("Spectrogram.png")

# def Exporter(self): 

                # data = (
                # ("First name", "Last name", "Age", "City"),
                #     ("Jules", "Smith", "34", "San Juan"),
                #     ("Mary", "Ramos", "45", "Orlando"),
                #     ("Carlson", "Banks", "19", "Los Angeles"),
                #     ("Lucas", "Cimon", "31", "Sain"),
                # )

                # pdf = FPDF()
                # pdf.add_page()
                # pdf.set_font("Times", size=10)
                # line_height = pdf.font_size * 2.5
                # col_width = 100 / 4 
                # for row in data:
                #     for datum in row:
                #         pdf.multi_cell(col_width, line_height, datum, border=1, ln=3, max_line_height=pdf.font_size)
                #     pdf.ln(line_height)
                # pdf.output('table_with_cells.pdf')
                

                # Import FPDF class

def Exporter(self): 
            FolderPath = QFileDialog.getSaveFileName( None, str('Save the signal file'), None, str("PDF FIles(*.pdf)"))
            if FolderPath != '':
                pdf = FPDF(format='letter', unit='in')
                
                # Add new page. Without this you cannot create the document
                pdf.add_page()

                # Style of the pdf
                # #pdf.set_font('ZapfDingbats','B',20)
                # pdf.set_font('Arial','B',20)
                # pdf.cell(70)
                # pdf.cell(50, 10, 'Signal Viewer Report', 0, 0, 'C')

                # #create a picture of the signal
                # ex3 = pg.exporters.ImageExporter(self.Plot.plotItem)
                # ex3.export('plot.png')

                # # insert the logos
                # pdf.image('Desgin/CUFE.png', 1, 1, 50, 40)
                # pdf.image('Desgin/logo.png', 160, 1, 50, 40)
                
                # # insert the plot graph and the specrogram
                # pdf.image('plot.png', 40, 50, 150, 100)
                # pdf.image('Spectrogram.png', 55, 160, 120, 100)

                # # Create instance of FPDF class
                # # Letter size paper, use inches as unit of measure
                

                # Add new page. Without this you cannot create the document.
                pdf.add_page()

                # Remember to always put one of these at least once.
                pdf.set_font('Times','',10.0) 

                # Effective page width, or just epw
                epw = pdf.w - 2*pdf.l_margin

                # Set column width to 1/4 of effective page width to distribute content 
                # evenly across table and page
                col_width = epw/6
                data = [['','Max','Min','Mean','Std_Dev','Duration'],[],[],[]]

                # Since we do not need to draw lines anymore, there is no need to separate
                # headers from data matrix.
                for index in range (3):
                    if self.ChannelLineArr[index].Filepath != "null":
                        data[index+1].append('Channel '+ str(index + 1))
                        data[index+1].append(round(np.amax(self.ChannelLineArr[index].Amplitude),4))
                        data[index+1].append(round(np.amin(self.ChannelLineArr[index].Amplitude),4))
                        data[index+1].append(round(np.mean(self.ChannelLineArr[index].Amplitude),4))
                        data[index+1].append(round(np.std(self.ChannelLineArr[index].Amplitude),4))
                        data[index+1].append(round(np.amax(self.ChannelLineArr[index].Time),4))

                        

              
                
                # data = [['','Max','Min','Std','Mean','Duration'],
                # ['Channel 1','Smith',34,'San Juan','',''],
                # ['Channel 2','Ramos',45,'Orlando','',''],[
                # 'Channel 3','Banks',19,'Los Angeles','','']
                # ]

                # Document title centered, 'B'old, 14 pt
                pdf.set_font('Times','B',14.0) 
                pdf.cell(epw, 0.0, 'Demographic data', align='C')
                pdf.set_font('Times','',10.0) 
                pdf.ln(0.5)

                # Text height is the same as current font size
                th = pdf.font_size

                for row in data:
                    for datum in row:
                        # Enter data in colums
                        # Notice the use of the function str to coerce any input to the 
                        # string type. This is needed
                        # since pyFPDF expects a string, not a number.
                        if datum == row[0]:
                            pdf.set_fill_color(200,200,200)
                            pdf.cell(col_width, 3*th, str(datum), border=1, fill=True)
                        elif row == data[0]:
                            pdf.set_fill_color(200,200,200)
                            pdf.cell(col_width, 3*th, str(datum), border=1, fill=True)
                        else:
                            pdf.cell(col_width, 3*th, str(datum), border=1)
                            

                    pdf.ln(3*th)

                # Line break equivalent to 4 lines
                #Exporting the Pdf
                pdf.output(str(FolderPath[0]))
                #pdf.output('table-using-cell-borders.pdf','F')

