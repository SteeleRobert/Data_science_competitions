import pandas as pd

filename = '../gps.csv'
#filename = 'wellness.csv'
#filename = 'rpe.csv'
#filename = 'games.csv'

data = pd.read_csv(filename, dtype={'GameID':int,'Half':int,'PlayerID':int,'FramID':int,'Speed':float, 'AccelImpulse':float, 'AccelLoad':float})

playerData = []

for i in range(1,18):
	for j in range(1,39):
		for k in range(1,3):
			tempData = data.loc[(data['PlayerID'] == i) & (data['GameID'] == j) & (data['Half'] == k) & (data['Speed'] != 0)]
			temp = [i,j,k,tempData['Speed'].mean(),len(tempData),tempData['AccelLoad'].mean(),tempData['AccelImpulse'].mean(),tempData['Speed'].max(),tempData['AccelLoad'].max(),tempData['AccelImpulse'].max()]
			playerData.append(temp)


save = pd.DataFrame(data=playerData,columns=['PlayerID','GameID','Half','AverageSpeed','TimeSpeed','AverageLoad','AverageImpulse','MaxSpeed','MaxLoad','MaxImpulse'])

save.to_csv('PlayerAveragesData.csv')
'''
players = []
gameTotalSpeed = []
gameTotalOccurranceSpeed = []
gameTotalOccurranceOther = []
gameAverageSpeed = []
maxSpeed = []

gameTotalLoad = []
gameAverageLoad = []
maxLoad = []

gameTotalImpulse = []
gameAverageImpulse = []
maxImpulse = []

for i in range(1,18):
	players.append(i)
	maxSpeed.append([])
	maxLoad.append([])
	maxImpulse.append([])
	gameTotalSpeed.append([])
	gameTotalLoad.append([])
	gameTotalImpulse.append([])
	gameTotalOccurranceSpeed.append([])
	gameTotalOccurranceOther.append([])
	for j in range(0,38):
		gameTotalSpeed[i-1].append(0)
		gameTotalLoad[i-1].append(0)
		gameTotalImpulse[i-1].append(0)
		gameTotalOccurranceSpeed[i-1].append(0)
		gameTotalOccurranceOther[i-1].append(0)
		maxSpeed[i-1].append(0)
		maxLoad[i-1].append(0)
		maxImpulse[i-1].append(0)


for i in data.index:
	pid = data.loc[i,'PlayerID']
	if pid in players:
		GID = data.loc[i,'GameID']
		if i % 200000 == 0:
			print(i)
		if data.loc[i,'Speed'] != 0:
			gameTotalSpeed[pid - 1][GID - 1] += data.loc[i,'Speed']
			if data.loc[i,'Speed'] > maxSpeed[pid - 1][GID-1]:
				maxSpeed[pid - 1][GID-1] = data.loc[i,'Speed']
			gameTotalOccurranceSpeed[pid - 1][GID-1] += 1
		
		gameTotalLoad[pid - 1][GID-1] += data.loc[i,'AccelLoad']
		gameTotalImpulse[pid - 1][GID-1] += data.loc[i,'AccelImpulse']
		gameTotalOccurranceOther[pid - 1][GID-1] += 1
		
		if data.loc[i,'AccelLoad'] > maxImpulse[pid - 1][GID-1]:
			maxLoad[pid - 1][GID-1] = data.loc[i,'AccelLoad']
		if data.loc[i,'AccelImpulse'] > maxLoad[pid - 1][GID-1]:
			maxImpulse[pid - 1][GID-1] = data.loc[i,'AccelImpulse']

total = 0

for i in range(0,17):
	gameAverageSpeed.append([])
	gameAverageLoad.append([])
	gameAverageImpulse.append([])
	for j in range(0,38):
		total += gameTotalOccurrance[i][j]
		if gameTotalOccurrance[i][j] != 0:
			gameAverageSpeed[i].append(gameTotalSpeed[i][j]/gameTotalOccurranceSpeed[i][j])
			gameAverageLoad[i].append(gameTotalLoad[i][j]/gameTotalOccurranceOther[i][j])
			gameAverageImpulse[i].append(gameTotalImpulse[i][j]/gameTotalOccurranceOther[i][j])
		else:
			gameAverageSpeed[i].append(0)
			gameAverageLoad[i].append(0)
			gameAverageImpulse[i].append(0)


playerData = []

for i in range(1,18):
	for j in range(1,38):
		temp = [i,j,gameAverageSpeed[i-1][j-1],gameTotalOccurranceSpeed[i-1][j-1],gameAverageLoad[i-1][j-1],gameAverageImpulse[i-1][j-1],maxSpeed[i-1],maxLoad[i-1],maxImpulse[i-1]]
		playerData.append(temp)

save = pd.DataFrame(data=playerData,columns=['GameID','PlayerID','AverageSpeed','TimeSpeed','AverageLoad','AverageImpulse','MaxSpeed','MaxLoad','MaxImpulse'])

save.to_csv('PlayerAveragesData.csv')
'''





	