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

# A function to return simillar movies
    
def create_movie_user_df(input_data, user1, user2):
      data = []
      for movie in input_data[user1].keys():
          if movie in input_data[user2].keys():
              try:
                  data.append( (movie
                  ,input_data[user1][movie]
                  ,input_data[user2][movie]) )
              except: 
                 pass
      return pd.DataFrame(data = data, columns = ['movie', user1,
                      user2])

df = create_movie_user_df(movie_user_preferences, 'Sam', 'William')
print(df)
    
# Plotting wrt to sam and william

plt.scatter(df.Sam, df.William)
plt.xlabel('Sam')
plt.ylabel('William')
for i, txt in enumerate(df.movie):
    plt.annotate(txt, (df.Sam[i], df.William[i]))
plt.show()

from scipy.stats import pearsonr

# Introduction to pearson correlation
s = pearsonr(df.Sam, df.William)

df1 = create_movie_user_df(movie_user_preferences, 'Sam', 'Julia')

# Plotting wrt Sam Julia

plt.scatter(df1.Sam, df1.Julia)
plt.xlabel('Sam')
plt.ylabel('Julia')
for i, txt in enumerate(df1.movie):
    plt.annotate(txt, (df1.Sam[i], df1.Julia[i]))
plt.show()


def sim_pearson(data, user1, user2):
    df3 = create_movie_user_df(data, user1, user2)
    s = pearsonr(df3[user1], df3[user2])
    if s[0] >= s[1]:
        return s[0]
    else:
        return s[1]    

pearson_score = sim_pearson(movie_user_preferences, 'Sam', 'Julia')
#print(pearson_score)


# Ranking the Users

def top_matches(data, user1, n = 5, similarity = sim_pearson):
    scores = [(similarity(data, user1, user2), user2)
    for user2 in data if user2 != user1]
    
    # Sorting 
    scores.sort()
    scores.reverse()
    return scores[0:n]

toby_top = top_matches(movie_user_preferences, 'Toby', n = 3, similarity = sim_pearson)
#print(toby_top)

# Get's recommendations for a person by using weighted average of every
# other user's ratings.

def getRecommendations(prefs,person,similarity=sim_pearson):
    totals={}
    simSums={}
    for other in prefs:
        # don't compare me to myself
        if other==person: continue
        sim=similarity(prefs,person,other)
        
        # ignore scores of zero or lower
        if sim<=0: continue
        for item in prefs[other]:
            
            # only score movies I haven't seen yet
            if item not in prefs[person] or prefs[person][item]==0:
                # Similarity * Score
                totals.setdefault(item,0)
                totals[item] += prefs[other][item]*sim
                # Sum of similarities
                simSums.setdefault(item,0)
                simSums[item] += sim
                
    # Create the normalized list
    rankings=[(total/simSums[item],item) for item,total in totals.items( )]
    
    # Return the sorted list
    rankings.sort( )
    rankings.reverse( )
    return rankings

recommendations_toby = getRecommendations(movie_user_preferences,'Toby')
print(recommendations_toby)
print("")
print("")


""" # Item Based Collaberative Filtering 

Item-based collaborative  ltering  nds the similarities between items. 
This is then used to  nd new recommendations for a user.

"""

# First we will invert the data, by putting movies first and users second.

def transform_data(data):
    result = {}
    for person in data:
        for movie in data[person]:
            result.setdefault(movie, {})
            result[movie][person] = data[person][movie]
    return result

user_movie_preferences = transform_data(movie_user_preferences)
print(user_movie_preferences)
print("")
print("")


# Create a dictionary to show items simillar to each other.

def calculate_similarity_items(data, n = 10):
    
    result = {}
    c = 0
    for item in data:
        c += 1
        if c%100 ==0:
            print("%d / %d" % (c,len(data)))
        scores = top_matches(data, item, n= n, similarity = sim_pearson)
        result[item] = scores
    return result

itemsim = calculate_similarity_items(user_movie_preferences, n = 10)
print(itemsim)
print("")
print("")

# Generating recommendation using item similarity

def get_recommendationItems(prefs,itemMatch,user):
       userRatings=prefs[user]
       scores={}
       totalSim={}
       # Loop over items rated by this user
       for (item, rating) in userRatings.items( ):
           
           # Loop over items similar to this one
           for (similarity, item2) in itemMatch[item]:
               
               # Ignore if this user has already rated this item
               if item2 in userRatings: continue
               
               # Weighted sum of rating times similarity
               scores.setdefault(item2, 0)
               scores[item2] += similarity*rating
               
               # Sum of all the similarities
               totalSim.setdefault(item2, 0)
               totalSim[item2] += similarity
                
            # Divide each total score by total weight to get an average
            
       rankings = [(score/totalSim[item], item) for item, score in scores.items()]
       rankings.sort()
       rankings.reverse()
       return rankings

recommendations = get_recommendationItems(movie_user_preferences, itemsim, 'Toby')
print(recommendations)
                
    
            





   

    



















