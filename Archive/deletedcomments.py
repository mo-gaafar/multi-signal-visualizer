#--------------------------------------------------------------- Table FUNCTIONS ---------------------------------------------------------------------------------------------------#

    # def createTable(self):
    #     self.tableWidget = QTableWidget()

    #     # Row count
    #     self.tableWidget.setRowCount(4)

    #     # Column count
    #     self.tableWidget.setColumnCount(2)

    #     self.tableWidget.setItem(0, 0, QTableWidgetItem(min))
    #     self.tableWidget.setItem(0, 1, QTableWidgetItem(max))
    #     self.tableWidget.setItem(1, 0, QTableWidgetItem("Aloysius"))
    #     self.tableWidget.setItem(1, 1, QTableWidgetItem("Indore"))
    #     self.tableWidget.setItem(2, 0, QTableWidgetItem("Alan"))
    #     self.tableWidget.setItem(2, 1, QTableWidgetItem("Bhopal"))
    #     self.tableWidget.setItem(3, 0, QTableWidgetItem("Arnavi"))
    #     self.tableWidget.setItem(3, 1, QTableWidgetItem("Mandsaur"))

#--------------------------------------------------------------- EXPORT FUNCTIONS --------------------------------------------------------------------------------------------------#

#     def ExportPDF(self):

#         # TODO make the messages valid
#         if self.pointsToAppend == 0:
#             QtWidgets.QMessageBox.warning(  self, 'NO SIGNAL ', 'You have to plot a signal first')
#         elif self.pointsToAppend != 0:
#             QtWidgets.QMessageBox.information(  self, 'Done', 'PDF has been created')
#        # create a CSV file of the signal
#             ex1 = pg.exporters.CSVExporter(self.Plot.plotItem)
#             ex1.export('test.csv')
#        # create a excell sheet of the signal
#             ex2 = pg.exporters.SVGExporter(self.Plot.plotItem)
#             ex2.export('test.svg')
#        # create a picture of the signal
#             ex3 = pg.exporters.ImageExporter(self.Plot.plotItem)
#             ex3.export('test.png')
#        # put the picture of the signal in an array
#         self.list = ['test.png']
#         # call the function create_pdf()

#         self.create_pdf()

# #--------------------------------------------------------------------------------CREATE TABLE------------------------------------------------------------#

    # def createTable(self):
    #     self.tableWidget = QTableWidget()

    #     # Row count
    #     self.tableWidget.setRowCount(4)

    #     # Column count
    #     self.tableWidget.setColumnCount(2)

    #     self.tableWidget.setItem(0, 0, QTableWidgetItem("Name"))
    #     self.tableWidget.setItem(0, 1, QTableWidgetItem("City"))
    #     self.tableWidget.setItem(1, 0, QTableWidgetItem("Aloysius"))
    #     self.tableWidget.setItem(1, 1, QTableWidgetItem("Indore"))
    #     self.tableWidget.setItem(2, 0, QTableWidgetItem("Alan"))5
    #     self.tableWidget.setItem(2, 1, QTableWidgetItem("Bhopal"))
    #     self.tableWidget.setItem(3, 0, QTableWidgetItem("Arnavi"))
    #     self.tableWidget.setItem(3, 1, QTableWidgetItem("Mandsaur"))

    # self.create_pdf()
#--------------------------------------------------------------------------------CREATE TABLE------------------------------------------------------------#

# def createTable(self):
#     self.tableWidget = QTableWidget()

#     # Row count
#     self.tableWidget.setRowCount(4)

#     # Column count
#     self.tableWidget.setColumnCount(2)

#     self.tableWidget.setItem(0, 0, QTableWidgetItem("Name"))
#     self.tableWidget.setItem(0, 1, QTableWidgetItem("City"))
#     self.tableWidget.setItem(1, 0, QTableWidgetItem("Aloysius"))
#     self.tableWidget.setItem(1, 1, QTableWidgetItem("Indore"))
#     self.tableWidget.setItem(2, 0, QTableWidgetItem("Alan"))
#     self.tableWidget.setItem(2, 1, QTableWidgetItem("Bhopal"))
#     self.tableWidget.setItem(3, 0, QTableWidgetItem("Arnavi"))
#     self.tableWidget.setItem(3, 1, QTableWidgetItem("Mandsaur"))

#     self.create_pdf()
#-----------------------------------------------------------------------------------------------------------------------------------#

# def create_pdf(self):
#     # the function that creates the pdf report
#     pdname = QFileDialog.getSaveFileUrl(
#         None, str('Save the signal file'), str("PDF FIles(*.pdf)"))
#     print(self.pdname[0])

#     if pdname != '':
#         pdf = FPDF()
#         # set pdf title
#         pdf.add_page()
#         pdf.set_font('Arial', 'B', 15)
#         pdf.cell(70)
#         pdf.cell(60, 10, 'Signal Viewer Report', 1, 0, 'C')
#         pdf.ln(5)
#        # pdf.cell(60, 10, 'Abdullah', 0, 0, 'L')

#         pdf.ln(20)

#         # put the graphs on the pdf
#         pdf.image('Desgin/CUFE.png', 1, 1, 50, 40)
#         pdf.image('Desgin/logo.png', 160, 1, 50, 40)

#         pdf.image('test.png', 40, 50, 100, 100)
#         pdf.image('Spectrogram.png', 40, 160, 100, 100)
#         pdf.output(str(pdname[0]))
#         # pdf.image()

# path = self.filename

# removes the graphs pictures as we dont need
# os.remove("test.png")
# os.remove("test.csv")
# os.remove("test.svg")
# os.remove('Spectrogram.png')

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
