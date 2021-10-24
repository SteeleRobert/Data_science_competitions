from scipy.signal import savgol_filter
import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

Y = []
wells = []
print('Load Data')
data = pd.read_csv('train.csv')



dataRows = []
dataLabels = []
print('Get Rows')
maxs = 0
for i in data['well_id'].unique():
    dt = data[data['well_id'] == i]['GR'].tolist()
    dataRows.append(dt)
    if(maxs < len(dt)):
        maxs = len(dt)
    dataLabels.append(data[data['well_id'] == i]['label'].tolist())
print(maxs)
print(len(dataRows))
print(len(dataRows[0]))
print('Put in data frame')

rowData = pd.DataFrame(dataRows)
#labels = pd.DataFrame(dataLabels)
print('done')
Y = rowData.iloc[1,:]

yhat = savgol_filter(np.asarray(Y), 21, 1) # window size 51, polynomial order 3

plt.plot(np.arange(0, len(Y)), Y)
plt.plot(np.arange(0, len(Y)), yhat, lw=4)
plt.show()

dy = np.gradient(yhat)
dyhat = savgol_filter(dy, 15, 1) # window size 51, polynomial order 3


plt.plot(np.arange(0, len(Y)), dyhat)
plt.show()


plt.plot(np.arange(0, len(Y)), np.gradient(yhat))
plt.show()