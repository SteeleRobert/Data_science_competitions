import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('PlayerSpeedLabels.csv')

data = data.groupby('Tournament').mean()

Tours = [ 'Dubai', 'Sydney','Commonwealth','Langford', 'Paris',  'World Cup']
avg = [0, 0, 0, 0, 0, 0]

for i in data.index:
	if i in Tours:
		avg[Tours.index(i)] = data.loc[i,'Speed']
		print(avg[Tours.index(i)])

tics = range(0,6)

avg = (avg-min(avg))/(max(avg)-min(avg))

plt.plot(avg)
plt.xticks(tics,Tours)
plt.title('Average Performance by Tournament')
plt.xlabel('Tournament')
plt.ylabel('Performance')
plt.show()
final = []

for i in range(0,len(avg)):
	final.append([avg[i],Tours[i]])

final = pd.DataFrame(final, columns=['AveragePerformance','Tournament'])

print(final)

final.to_csv('AveragePerformanceByTournament.csv')