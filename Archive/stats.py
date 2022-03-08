from itertools import count
import statistics
from PyQt5.QtWidgets import * 

import sys
from PyQt5.QtWidgets import *

from matplotlib import axes
import pandas as pd
import matplotlib.pyplot as plt


#Main Window
class App(QWidget):
	def __init__(self):
		super().__init__()
		self.title = 'PyQt5 - QTableWidget'
		self.left = 0
		self.top = 0
		self.width = 600
		self.height = 500

		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)

		self.createTable()

		self.layout = QVBoxLayout()
		self.layout.addWidget(self.tableWidget)
		self.setLayout(self.layout)

		#Show window
		self.show()

	#Create table
	def createTable(self):
		
		df = pd.read_csv('test.csv')
		self.E= df.describe()
		self.tableWidget = QTableWidget()

		#Row count
		self.tableWidget.setRowCount(4)

		#Column count
		self.tableWidget.setColumnCount(2)

		self.tableWidget.setItem(0,0, QTableWidgetItem(min(self.E)))
		self.tableWidget.setItem(0,1, QTableWidgetItem(max(self.E)))
		# self.tableWidget.setItem(1,0, QTableWidgetItem(stdev(self.E)))
		# self.tableWidget.setItem(1,1, QTableWidgetItem(mean(self.E)))
		# self.tableWidget.setItem(2,0, QTableWidgetItem(count(self.E)))
		# self.tableWidget.setItem(0,0, QTableWidgetItem("Bhopal"))
		# self.tableWidget.setItem(0,1, QTableWidgetItem("Bhopal"))
		self.tableWidget.setItem(1,0, QTableWidgetItem("Bhopal"))
		self.tableWidget.setItem(1,1, QTableWidgetItem("Bhopal"))
		self.tableWidget.setItem(2,0, QTableWidgetItem("Bhopal"))
		self.tableWidget.setItem(2,1, QTableWidgetItem("Bhopal"))
		self.tableWidget.setItem(3,0, QTableWidgetItem("Arnavi"))
		self.tableWidget.setItem(3,1, QTableWidgetItem("Mandsaur"))

		#Table will fit the screen horizontally
		self.tableWidget.horizontalHeader().setStretchLastSection(True)
		self.tableWidget.horizontalHeader().setSectionResizeMode(
			QHeaderView.Stretch)

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())


# data = [1,2,3,4,5,6,7,8,9,10]
# minn = min(data)
# maxx = max(data)
# stdev = statistics.mean(data)
# statistics.stdev(data)
# print('min')
# print(minn)
# print('max')
# print(maxx)
# print('stdev')
# print(stdev)




# s = pd.Series([1, 2, 3])