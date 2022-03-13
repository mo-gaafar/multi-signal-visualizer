import sys

from PyQt5.QtWidgets import (QVBoxLayout, QMainWindow, QWidget, QApplication)
import pyqtgraph as pg


class plotAndTableWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.create_data()

    def initUI(self):
        self.central_widget = QWidget()
        self.vertical_layout = QVBoxLayout()
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(self.vertical_layout)
        self.plot = pg.PlotWidget()
        self.table = pg.TableWidget()
        
        #The 1 after the plot and table essentially tells Qt to expand
        #those widgets evenly so they should take up a similar amount of space.
        # self.vertical_layout.addWidget(self.plot, 1)
        self.vertical_layout.addWidget(self.table, 7)

    def create_data(self):
        data = {'col1':[1, 2, 3, 4],
                'col2':[1, 2, 1, 3],
                'col3':[1, 1 ,2, 1]}
        self.table.setData(data)
        
        for i in data.keys():
            self.plot.plot(y=data[i])

def run_program():
    app = QApplication(sys.argv)
    window = plotAndTableWidget()
    window.show()
    app.exec()
    #If you want to close your python interpreter you will need to add
    #sys.exit(app.exec_()) instead of app.exec().

if __name__ == '__main__':
    run_program()