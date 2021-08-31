# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 08:27:19 2020

@author: Ted
"""
import pickle
import numpy as np
from tqdm import tqdm

with open('muser_ratings.pkl', 'rb') as handle:
    user_dict = pickle.load(handle)
with open('scores.p', 'rb') as handle1:
    movie_dict = pickle.load(handle1)
    #Assumes of the form movieID:subspace score


def get_user_score_dict(user_dict,movie_dict):
    user_score_dict={}
    for user in tqdm(user_dict.keys()):
        users_ratings=user_dict[user]
        
        user_subspace_score = np.array([0.,0.,0.,0.,0.])
        for movieID,rating in users_ratings:
            try:
                movie_subspace_scores = movie_dict[int(movieID)]
                movie_subspace_score=(movie_subspace_scores[0]+movie_subspace_scores[1])/2
                normalized_rating = (rating-3.53)/1.066
                user_subspace_score+= normalized_rating * movie_subspace_score
            except: 
                pass                
        user_subspace_score=np.clip(user_subspace_score,-1,1)
        user_score_dict[user]=user_subspace_score
        
    return user_score_dict

user_score_dict= get_user_score_dict( user_dict,movie_dict)     
with open('user_subspace_scores.pkl', 'wb') as handle1:
    pickle.dump(user_score_dict, handle1, pickle.HIGHEST_PROTOCOL)
