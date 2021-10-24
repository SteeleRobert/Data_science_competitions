import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

filename = '../gps.csv'
#filename = 'wellness.csv'
#filename = 'rpe.csv'
#filename = 'games.csv'

gps = pd.read_csv(filename, dtype={'GameID':int,'Half':int,'PlayerID':int,'FramID':int,'Speed':float, 'AccelImpulse':float, 'AccelLoad':float, 'AccelX':float, 'AccelY':float, 'AccelZ':float, 'Latitude':float, 'Longitude':float})
games = pd.read_csv('games.csv')
avg_max = pd.read_csv('PlayerAveragesData.csv',dtype={'AverageSpeed':float,'AverageImpulse':float,'AverageLoad':float})

PlayerData = []

for Player in range(1,18):
	maxSpeed = avg_max.loc[avg_max['PlayerID'] == Player]['MaxSpeed'].max()*.75
	tourny = []
	tournySpeeds = []
	gamesPlayed = 0
	tournyAvgSpeeds = []
	tournyAvgImpulse = []
	tournyAvgLoad = []
	tournyOccurrance = []

	for i in range(1,len(games)+1):
		tour = games.loc[games['GameID'] == i]['Tournament'].to_string().split()[1]
		if(tour not in tourny):
			tourny.append(tour)
			tournySpeeds.append(0)
			tournyAvgSpeeds.append(0)
			tournyAvgImpulse.append(0)
			tournyAvgLoad.append(0)
			tournyOccurrance.append(0)
		
		if(len(gps.loc[(gps['PlayerID'] == Player) & (gps['GameID'] == i) & (gps['Speed'] > maxSpeed)]) != 0):
			tournySpeeds[tourny.index(tour)] += len(gps.loc[(gps['PlayerID'] == Player) & (gps['GameID'] == i) & (gps['Speed'] > maxSpeed)])
			print(avg_max.loc[(avg_max['PlayerID'] == Player) & (avg_max['GameID'] == i) & (avg_max['Half'] == 1)]['AverageSpeed'])
			tournyAvgSpeeds[tourny.index(tour)] += avg_max.loc[(avg_max['PlayerID'] == Player) & (avg_max['GameID'] == i) & (avg_max['Half'] == 1)]['AverageSpeed'] + avg_max.loc[(avg_max['PlayerID'] == Player) & (avg_max['GameID'] == i) & (avg_max['Half'] == 2)]['AverageSpeed']
			tournyAvgImpulse[tourny.index(tour)] += avg_max.loc[(avg_max['PlayerID'] == Player) & (avg_max['GameID'] == i) & (avg_max['Half'] == 1)]['AverageImpulse'] + avg_max.loc[(avg_max['PlayerID'] == Player) & (avg_max['GameID'] == i) & (avg_max['Half'] == 2)]['AverageImpulse']
			tournyAvgLoad[tourny.index(tour)] += avg_max.loc[(avg_max['PlayerID'] == Player) & (avg_max['GameID'] == i) & (avg_max['Half'] == 1)]['AverageLoad'] + avg_max.loc[(avg_max['PlayerID'] == Player) & (avg_max['GameID'] == i) & (avg_max['Half'] == 2)]['AverageLoad']
			tournyOccurrance[tourny.index(tour)] += 1


	for i in range(0,len(tourny)):
		if(tournyOccurrance[i] != 0):
			PlayerData.append([Player, i, tourny[i], tournySpeeds[i]/tournyOccurrance[i], tournyAvgSpeeds[i]/tournyOccurrance[i], tournyAvgImpulse[i]/tournyOccurrance[i], tournyAvgLoad[i]/tournyOccurrance[i]])
		else:
			PlayerData.append([Player, i, tourny[i], 0, 0, 0, 0])


save = pd.DataFrame(data=PlayerData,columns=['PlayerID','TournamentID','Tournament','SprintTime','AverageSpeed','AverageImpulse','AverageLoad'])

save.to_csv('PlayerTournamentAverages.csv')


