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


maxPlayer = result.groupby(['PlayerID', 'Tournament']).mean()




realFinal.to_csv('PlayerAccelerationLabelsWithout.csv')
