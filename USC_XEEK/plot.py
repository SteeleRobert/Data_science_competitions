import numpy as np
import matplotlib.pyplot as plt
import csv

Y = []
Y2 = []

with open("test.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        try:
            Y.append(float(row[2]))
        except:
            print("error!2")

with open("submission.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        Y2.append(float(row[3]))

Y = np.asarray(Y)
Y2 = np.asarray(Y2)

Y = (Y-np.mean(Y))/np.std(Y) + 2

plt.plot(np.arange(len(Y)), Y)
plt.plot(np.arange(len(Y2)), Y2)
plt.show()
