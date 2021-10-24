import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

filename = '../gps.csv'
#filename = 'wellness.csv'
#filename = 'rpe.csv'
#filename = 'games.csv'

gps = pd.read_csv(filename, dtype={'GameID':int,'Half':int,'PlayerID':int,'FramID':int,'Speed':float, 'AccelImpulse':float, 'AccelLoad':float, 'AccelX':float, 'AccelY':float, 'AccelZ':float, 'Latitude':float, 'Longitude':float})
games = pd.read_csv('games.csv')
wellness = pd.read_csv('wellness.csv')
avg_max = pd.read_csv('PlayerAveragesData.csv')

Player  = 1
maxSpeed = avg_max.loc[avg_max['PlayerID' == Player]]['MaxSpeed'].max()*75

dateFeel = []
fatigue = []
soreness = []

highSpeeds = []
dateSpeeds = []

for i in range(1,len(games)+1):
	highSpeed = len(gps.loc[(gps['PlayerID'] == Player) & (gps['GameID'] == i) & (gps['Speed'] > maxSpeed)])
	date = pd.to_datetime(games.loc(games['GameID'] == i)['Date'], format='%m/%d/%Y')
	dateSpeeds.append(date)
	highSpeeds.append(highSpeed)

	dateUp = date.timedelta(days=1)
	dateDown = date.timedelta(days=-1)

	fatigue.append(wellness.loc((wellness['Date'] == dateDown.strftime("%m/%d/%Y")) & (wellness['PlayerID'] == Player))['Fatigue'])
	fatigue.append(wellness.loc((wellness['Date'] == date.strftime("%m/%d/%Y")) & (wellness['PlayerID'] == Player))['Fatigue'])
	fatigue.append(wellness.loc((wellness['Date'] == dateUp.strftime("%m/%d/%Y")) & (wellness['PlayerID'] == Player))['Fatigue'])
	soreness.append(wellness.loc((wellness['Date'] == dateDown.strftime("%m/%d/%Y")) & (wellness['PlayerID'] == Player))['Soreness'])
	soreness.append(wellness.loc((wellness['Date'] == date.strftime("%m/%d/%Y")) & (wellness['PlayerID'] == Player))['Soreness'])
	soreness.append(wellness.loc((wellness['Date'] == dateUp.strftime("%m/%d/%Y")) & (wellness['PlayerID'] == Player))['Soreness'])
	dateFeel.append(dateDown)
	dateFeel.append(date)
	dateFeel.append(dateUp)

plt.plot(highSpeeds,dateSpeeds)
plt.show()

