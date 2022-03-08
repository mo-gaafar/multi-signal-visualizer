

from matplotlib import axes
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('test.csv')
e=df.describe()
print(e)  
#print(pd.DataFrame.count)  

# pd.plotting.table(axes, df, rowLabels=None, colLabels=None, )

# s = pd.Series([1, 2, 3])
# print(s.describe())
# def save(self):
#         document = SimpleDocTemplate("report.pdf", pagesize=letter)
#         items = [] 
#         #self.mean, self.std_dev, self.min_amplitude, self.max_amplitude, self.duration = self.data_stats(self.y_txt,self.x_txt)     
#         self.min_amplitude, self.max_amplitude, self.duration = self.data_stats(self.y_csv, self.x_csv) 
#         # self.mean, self.std_dev, self.min_amplitude, self.max_amplitude, self.duration = self.data_stats(self.y_xls, self.x_xls) 
#         data= [['','Mean', 'Standard Devition', 'Minimum', 'Maximum', 'Duration'],
#         ['Channel 1','', '', self.min_amplitude, self.max_amplitude, self.duration]]
#         # ['Channel 2',self.mean, self.std_dev, self.min_amplitude, self.max_amplitude, self.duration],
#         # ['Channel 3',self.mean, self.std_dev, self.min_amplitude, self.max_amplitude, self.duration]]
#         t=Table(data,6*[1.5*inch], 2*[0.5*inch])
#         t.setStyle(TableStyle([('ALIGN',(1,1),(-2,-2),'RIGHT'),
#         ('VALIGN',(0,0),(-1,-1),'CENTER'),
#         ('ALIGN',(0,0),(-1,-1),'CENTER'),
#         ('VALIGN',(0,0),(-1,-1),'TOP'),
#         ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
#         ('BOX', (0,0), (-1,-1), 0.25, colors.black),]))
#         items.append(t)
#         document.build(items)

#         pdf = matplotlib.backends.backend_pdf.PdfPages("output.pdf")
#         pdf.savefig(self.getFigure())
#         pdf.close()

        # report = PdfPages('figures.pdf') # make user choose name(?)
        # for signal in self.signals:
        #     report.savefig(signal.getFigure())
        #     report.savefig(signal.getSpectrogram())
        # report.close()