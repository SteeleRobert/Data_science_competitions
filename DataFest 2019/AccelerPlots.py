import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

filename = '../gps.csv'
#filename = 'wellness.csv'
#filename = 'rpe.csv'
#filename = 'games.csv'

data = pd.read_csv(filename, dtype={'GameID':int,'Half':int,'PlayerID':int,'FramID':int,'Speed':float, 'AccelImpulse':float, 'AccelLoad':float, 'AccelX':float, 'AccelY':float, 'AccelZ':float, 'Latitude':float, 'Longitude':float})

for j in range(2,18):
	P1G1 = data.loc[(data['PlayerID'] == j) & (data['GameID'] == 1) & (data['Half'] == 2) & (data['Speed'] != 0)]

	FrameID = []

	allData = []
	allData.append([])
	allData.append([])
	allData.append([])
	allData.append([])

	for i in P1G1.loc[:,'FrameID']:
		FrameID.append(i)

	for i in P1G1.loc[:,'AccelImpulse']:
		allData[0].append(i)

	for i in P1G1.loc[:,'AccelLoad']:
		allData[1].append(i)

	for i in P1G1.loc[:,'Speed']:
		allData[2].append(i)

	for i in P1G1.loc[:,'AccelX']:
		allData[3].append(i)

	plt.subplot(4,4,j-1)
	plt.scatter(FrameID, allData[2], c='g')


scaler = MinMaxScaler()

#allData = scaler.fit_transform(allData)


#plt.scatter(FrameID, allData[0], c='r')
#plt.scatter(FrameID, allData[1], c='b')
#plt.scatter(FrameID, allData[2], c='g')
#plt.scatter(FrameID, allData[3], c='r')


#plt.hist(allData[0], 20)
#plt.hist(allData[1], 100)
#plt.hist(allData[2], 20)

plt.show()