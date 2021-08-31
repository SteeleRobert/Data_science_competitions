import pandas as pd
import numpy as np
from tqdm import tqdm
from geopy.distance import geodesic
from scipy.spatial.distance import pdist, squareform
from sklearn.cluster import DBSCAN 
tqdm.pandas()

venues = pd.read_csv('data/venues.csv')

public_transport = ['train_station','transit_station','subway_station','light_rail_station','bus_station']
major_dest = ['zoo','stadium','museum','amusement_park','aquarium','natural_feature']
food = ['restaurant','grocery_or_supermarket','food','bakery','meal_takeaway','meal_delivery','cafe',
]
night_life = ['night_club','bar']
shopping = ['department_store','electronics_store','home_goods_store','shoe_store',
            'convenience_store','book_store','clothing_store','furniture_store','hardware_store',
           'pet_store','jewelry_store','bicycle_store','store','liquor_store',
            'shopping_mall','movie_rental','atm',]
minor_dest = ['hair_care','spa','art_gallery','movie_theater',"'park'",'beauty_salon','casino','bowling_alley',]
business = ['accounting',
 'pharmacy',
 'funeral_home',
 'electrician',
 'locksmith',
 'finance',
 'storage',
 'laundry',
'insurance_agency',
 'hospital',
 'health',
 'real_estate_agency',
 'roofing_contractor',
'car_repair',
 'lawyer',
 'bank',
'car_rental',
 'moving_company',
 'gym',
'plumber',
 'establishment',
 'physiotherapist',
 'gas_station',
 'car_wash',
 'general_contractor',
 'car_dealer',
 'dentist',
 'travel_agency',
  'doctor',
 'subpremise',
  'veterinary_care','painter','premise','florist',
]
govt = ['courthouse',
 'local_government_office',
       'post_office',
 'political',
 'embassy',
 'police','airport',
 'library', 'city_hall',]
religion = ['place_of_worship','cemetery', 'synagogue',
 'church',]
lodging = ['rv_park',
 'lodging','campground',]
edu = ['university','school',  ]




def get_dbscan_labels(venue_list, ven_type, city, epsilon=0.1, min_samples=5):
    ven = venues[venues['types'].str.contains('|'.join(venue_list))]
    dic = dict()
    for i in ven['city'].unique():
        dic[i] = ven[ven['city'] == i]
    labels_dict = dict()

    coords = dic[city][['latitude', 'longitude']].to_numpy()
    print('compute distance')
    distance_matrix = squareform(pdist(coords, (lambda u,v: geodesic(u,v).km)))
    np.save(ven_type + '_' + city + '.npy', distance_matrix)
    print('DBscan')



venues_types = {'public_transport':public_transport,'shopping':shopping,'major_dest':major_dest,'food':food,'night_life':night_life,'minor_dest':minor_dest}
cities = venues['city'].unique()
vens_t = ['shopping']
for city in cities:
    for ven_type in vens_t:
        get_dbscan_labels(venues_types[ven_type], ven_type, city)

