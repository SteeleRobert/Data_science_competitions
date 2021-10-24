import pandas as pd

filename = '../gps.csv'
#filename = 'wellness.csv'
#filename = 'rpe.csv'
#filename = 'games.csv'

data = pd.read_csv(filename, dtype={'GameID':int,'Half':int,'PlayerID':int,'FramID':int,'Speed':float, 'AccelImpulse':float, 'AccelLoad':float})
games = pd.read_csv('games.csv')

data = data.drop(columns=['Time', 'GameClock'])
games = games.drop(columns=['Team','Opponent', 'Outcome', 'TeamPoints', 'TeamPointsAllowed','TournamentGame','Date'])

result = pd.merge(data, games, on='GameID', how='outer')
maxPlayer = result.groupby(['PlayerID']).max()

maxPlayer = maxPlayer.drop(columns=['GameID', 'Half', 'FrameID', 'AccelImpulse', 'AccelLoad','AccelX', 'AccelY', 'AccelZ', 'Longitude', 'Latitude', 'Tournament'])

maxPlayer = maxPlayer.drop(index=[18,19,20,21])


overMax = pd.merge(result, maxPlayer, on='PlayerID', how='outer')
overMax = overMax[overMax['Speed_x'] > overMax['Speed_y']*.75]

playGame = data.drop(columns = ['Half', 'FrameID', 'AccelImpulse', 'AccelLoad','AccelX', 'AccelY', 'AccelZ', 'Longitude', 'Latitude'])



overMax = overMax.groupby(['PlayerID','GameID'],as_index=False).count()


overMax = overMax.drop(columns=['Tournament'])

overMax = pd.merge(overMax, games, on='GameID', how='outer')


overMaxTourn = overMax.groupby(['PlayerID','Tournament'],as_index=False).agg(['sum', 'count'])

totalSpeed = overMaxTourn.loc[:,['Half', 'sum']]

#print(totalSpeed)

#print(totalSpeed.index)


#drop langford and paris

final = totalSpeed.drop(index=['langford','Paris','Kitakyushu'], level=1)

idx = pd.IndexSlice

divide = []

i = 0
for PID in final.index:
	divide.append([PID[0],PID[1],(final.loc[idx[PID[0],PID[1]], idx['Half','sum']]/final.loc[idx[PID[0],PID[1]], idx['Half','count']])])


finalData = pd.DataFrame(divide, columns=['PlayerID','Tournament','Speed'])

#print(finalData)
stdev = []
avg = []

for i in final.index.droplevel(1).unique():
	if(len(finalData.loc[finalData['PlayerID'] == i]['Speed']) == 1):
		stdev.append(finalData.loc[finalData['PlayerID'] == i]['Speed'].max())
	else:
		stdev.append(finalData.loc[finalData['PlayerID'] == i]['Speed'].std())
	avg.append(finalData.loc[finalData['PlayerID'] == i]['Speed'].mean())

labels = []


for i in range(0,len(finalData.index)):
	playerid = finalData.loc[i,:]['PlayerID'].max()
	Tournament = finalData.loc[i,:]['Tournament']
	if avg[playerid-1]-stdev[playerid-1] > finalData.loc[i,'Speed']:
		labels.append([playerid,Tournament,-1])
	elif avg[playerid-1]+stdev[playerid-1] < finalData.loc[i,'Speed']:
		labels.append([playerid,Tournament,1])
	else:
		labels.append([playerid,Tournament,0])

label = pd.DataFrame(labels, columns=['PlayerID','Tournament','Label'])


realFinal = pd.merge(label,finalData, on=['Tournament','PlayerID'], how='outer')

print(realFinal)


realFinal.to_csv('PlayerSpeedLabelsWithoutKPL.csv')

