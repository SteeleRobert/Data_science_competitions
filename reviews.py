import pandas as pd
from tqdm import tqdm

imdb = pd.read_csv('data/imdb_review.csv')
movie_index = imdb.set_index('movieid')
temp_list= []
movie_ids = imdb['movieid'].unique()
inds = int(len(movie_ids)/4)
ind = 0
for movie in tqdm(movie_ids[inds*ind:inds*(ind+1)]):
    temp = movie_index.loc[movie]
    reviews = ''
    for i in temp.head(50):
        reviews += i + ' '
    temp_list.append({'movieid': movie, 'reviews': reviews})
top50 = pd.DataFrame(temp_list)
top50.to_csv('data/filtered_reviews.csv')