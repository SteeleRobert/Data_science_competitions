import pandas as pd
from geopy.distance import geodesic
from tqdm import tqdm
tqdm.pandas()

listings = pd.read_csv('data/listings.csv')
venues = pd.read_csv('data/venues.csv')

def get_dist(row,lat,long):
    return geodesic((lat,long), (row['latitude'], row['longitude'])).km

vens = dict()
for i in venues['city'].unique():
    vens[i] = venues[venues['city'] == i]

def top_business(row, top):
    ven = vens[row['metropolitan']]
    dist = ven.apply(lambda x: get_dist(x, row['latitude'], row['longitude']), axis=1).sort_values(ascending=False).head(top)
    return str(dist)

distances = listings.progress_apply(lambda x: top_business(x, 20), axis =1 )

distance.to_csv('distance.csv')