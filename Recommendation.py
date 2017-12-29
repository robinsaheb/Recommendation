#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 29 20:13:14 2017

@author: sahebsingh
"""

movie_user_preferences={'Jill': {'Avenger: Age of Ultron': 7.0,
 'Django Unchained': 6.5,
 'Gone Girl': 9.0,
 'Kill the Messenger': 8.0},
'Julia': {'Avenger: Age of Ultron': 10.0,
 'Django Unchained': 6.0,
 'Gone Girl': 6.5,
 'Kill the Messenger': 6.0,
 'Zoolander': 6.5},
'Max': {'Avenger: Age of Ultron': 7.0,
 'Django Unchained': 7.0,
 'Gone Girl': 10.0,
 'Horrible Bosses 2': 6.0,
 'Kill the Messenger': 5.0,
 'Zoolander': 10.0},
'Robert': {'Avenger: Age of Ultron': 8.0,
 'Django Unchained': 7.0,
 'Horrible Bosses 2': 5.0,
 'Kill the Messenger': 9.0,
 'Zoolander': 9.0},
'Sam': {'Avenger: Age of Ultron': 10.0,
 'Django Unchained': 7.5,
 'Gone Girl': 6.0,
 'Horrible Bosses 2': 3.0,
 'Kill the Messenger': 5.5,
 'Zoolander': 7.0},
'Toby': {'Avenger: Age of Ultron': 8.5,
 'Django Unchained': 9.0,
 'Zoolander': 2.0},
'William': {'Avenger: Age of Ultron': 6.0,
             'Django Unchained': 8.0,
 'Gone Girl': 7.0,
 'Horrible Bosses 2': 4.0,
 'Kill the Messenger': 6.5,
 'Zoolander': 4.0}}

movie_user_preferences['William']['Gone Girl']
7.0

data = []
for i in movie_user_preferences:
    try:
        data.append((i, 
                    movie_user_preferences[i]['Django Unchained'],
                    movie_user_preferences[i]['Avenger: Age of Ultron']))
    except:
        pass

import pandas as pd
import matplotlib.pyplot as plt

df = pd.DataFrame(data = data, columns =  ['user', 'django',
                       'avenger'])
print(df)

plt.scatter(df['django'], df['avenger'])
plt.xlabel('Django')
plt.ylabel('Avengers')
for i, txt in enumerate(df.user):
    plt.annotate(txt, (df['django'][i], df['avenger'][i]))
plt.show()

from math import sqrt

# Euclidean Distance Between Jill and Toby rating

print(sqrt(pow(8.5-7,2)+pow(9-6.5,2)))

# Euclidean Distance Between Robert and Max rating

print(sqrt(pow(8-7,2)+pow(7-7,2)))

# Similarity Score Between Jill and Toby 

print(1/(1 + sqrt(pow(8.5-7,2)+pow(9-6.5,2))))

# Similarity Score Between Robert and Max

print(1/ (1 + (sqrt(pow(8-7,2)+pow(7-7,2)))))

# Returns a distance-based similarity between person1 and person2

def sim_distance(prefs, person1, person2):
    # Get the list of shared_item
    si = {}
    for item in prefs[person1]:
        for item in prefs[person2]:
            si[item] = 1
    # If they have no rating in common return 0
    if len(si) ==0:
        return 0
    
    # Add up the squares of all the difference
    sum_of_squares=sum([pow(prefs[person1][item] -
                           prefs[person2][item])
      for item in prefs[person1] if item in prefs[person2]])
    
    return 1/(1 + sum_of_squares)

    

    



















