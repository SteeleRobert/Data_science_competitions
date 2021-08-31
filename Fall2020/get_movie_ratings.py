# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 14:14:07 2020

@author: Ted
"""

import pandas as pd
from collections import defaultdict
import pickle
from tqdm import tqdm
tags=pd.read_csv("ratings.csv")
tags=tags.drop(columns=['timestamp'])
user_dict={}

for userid,group in tqdm(tags.groupby("userId")):
    if len(group)>25:
        subset = group[['movieId', 'rating']]
        tuples = [tuple(x) for x in subset.to_numpy()]
        user_dict[userid]=tuples
with open('muser_ratings.pkl', 'wb') as f:
        pickle.dump(user_dict, f, pickle.HIGHEST_PROTOCOL)
