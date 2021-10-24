from scipy.signal import savgol_filter
import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

Y = []
wells = []
data = pd.read_csv('train.csv')



dataRows = []
dataLabels = []

maxs = 0
i =data['well_id'].unique()[0]
dt = data[data['well_id'] == i]['GR'].tolist()
dataRows.append(dt)
if(maxs < len(dt)):
    maxs = len(dt)
dataLabels.append(data[data['well_id'] == i]['label'].tolist())


rowData = pd.DataFrame(dataRows)
labels = pd.DataFrame(dataLabels)
vertlines = [[],[],[],[],[]]
for i in range(len(labels.columns)-1):
    if(labels.iloc[0,i] != labels.iloc[0,i+1]):
    	vertlines[labels.iloc[0,i]].append(i)
    	vertlines[labels.iloc[0,i+1]].append(i+1)

print(vertlines)

Y = rowData.iloc[0,:]

yhat = savgol_filter(np.asarray(Y), 21, 1) # window size 51, polynomial order 3

plt.plot(np.arange(0, len(Y)), Y)
plt.plot(np.arange(0, len(Y)), yhat, lw=4)
plt.show()

dy = np.gradient(yhat)
dyhat = savgol_filter(dy, 15, 1) # window size 51, polynomial order 3


plt.plot(np.arange(0, len(Y)), dyhat)
for xc in vertlines[0]:
    plt.axvline(x=xc, color='red')
for xc in vertlines[1]:
    plt.axvline(x=xc, color='green')
for xc in vertlines[2]:
    plt.axvline(x=xc, color='yellow')
for xc in vertlines[3]:
    plt.axvline(x=xc, color='purple')
for xc in vertlines[4]:
    plt.axvline(x=xc, color='black')
plt.show()


plt.plot(np.arange(0, len(Y)), np.gradient(yhat))
for xc in vertlines[0]:
    plt.axvline(x=xc, color='red')
for xc in vertlines[1]:
    plt.axvline(x=xc, color='green')
for xc in vertlines[2]:
    plt.axvline(x=xc, color='yellow')
for xc in vertlines[3]:
    plt.axvline(x=xc, color='purple')
for xc in vertlines[4]:
    plt.axvline(x=xc, color='black')
plt.show()