

from matplotlib import axes
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('test.csv')
e=df.describe()
#print(e.min)  
#print(pd.DataFrame.count)  

pd.plotting.table(axes, df, rowLabels=None, colLabels=None, )

# s = pd.Series([1, 2, 3])
# print(s.describe())
