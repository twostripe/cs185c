import	csv
import	sys
import	warnings
import	threading	as	th
import collections
from random import randint
from random import random
import matplotlib.pyplot as plt

import numpy as np

import os

## CREATE music collections
# collection = songs from a set of playlists, with playcount
# playlist = list of songs (no repetitions)

dir = ""
song_list = np.array(list(csv.reader(open(os.path.join(dir, "songs.csv"), 'rt'))))
#song_list = np.array(list(csv.reader(open(os.path.join(dir, "songs_limited.csv"), 'rt')))) # a limited subset of the songs to make things quicker and more impressive (more chance for repetition)
header = np.array(list(csv.reader(open(os.path.join(dir, "header.csv"), 'rt'))))

songs = collections.OrderedDict()
songs_by_id = {}
for song in song_list:
    songs[song[1]] = {'name': song[3], 'artist': song[2]}
    songs_by_id[song[1]] = {'id': song[1], 'name': song[3], 'artist': song[2]}



### FUNCTION DEFINITIONS

## returns a playlist of a specific genre of a specified number of songs
def build_playlist(genre, num_songs):
    # the genre we're looking for
    # (change this)
    genre_list = []
    
    # put all the songs of a particular genre to one side
    i = 0
    for the_song in song_list :
        if the_song[0] == genre :
            genre_list.append({'id': the_song[1], 'name': the_song[3], 'artist': the_song[2]})

    playlist = []
    
    i = 0
    for i in range(0,num_songs) :
        playlist.append(genre_list[randint(0,len(genre_list)-1)])
        
    return playlist

# builds a collection of playlists with two genres of a specified proportion
def build_playlist_set(genre_1, genre_proportion_1, genre_2, genre_proportion_2):
    num_playlists = 20
    playlist_set = []

    proportion_total = genre_proportion_1 + genre_proportion_2

    int = 0
    for i in range(0,20): 
        genre = ""
        if (proportion_total * random() < genre_proportion_1):
            genre = genre_1
        else:
            genre = genre_2
        
        playlist_set.append(build_playlist(genre, 15))
        
    return playlist_set



# make a few collections of playlists with varying amounts of "hip-hop" and "pop"
playlists_collection = {}
playlists_collection['0z'] = build_playlist_set("hip-hop", 0, "pop", 1)
playlists_collection['Alfrig'] = build_playlist_set("hip-hop", .1, "pop", .9)
playlists_collection['Barney'] = build_playlist_set("hip-hop", .2, "pop", .8)
playlists_collection['Cynthia'] = build_playlist_set("hip-hop", .3, "pop", .7)
playlists_collection['Dennerys'] = build_playlist_set("hip-hop", .4, "pop", .6)
playlists_collection['Elsie'] = build_playlist_set("hip-hop", .5, "pop", .5)
playlists_collection['Fenna'] = build_playlist_set("hip-hop", .6, "pop", .4)
playlists_collection['Greggory'] = build_playlist_set("hip-hop", .7, "pop", .3)
playlists_collection['Hal'] = build_playlist_set("hip-hop", .8, "pop", .2)
playlists_collection['IO'] = build_playlist_set("hip-hop", .9, "pop", .1)
playlists_collection['Joan'] = build_playlist_set("hip-hop", 1, "pop", 0)

# build "master list"
# generate "taste" for each person
# (we are!)
def build_master_list(master_playlist):
    # master_playlist should be a list of playlistslists, each containing a song
    master_list = {}

    for playlist in master_playlist:
        for song in playlist:
            
            # check to see if we already have the song (by id)
            if (song['id'] in master_list):
                master_list[song['id']] = master_list[song['id']] + 1
            else: 
                master_list[song['id']] = 1
            
#    for song in master_list: print(song + ", " + str(master_list[song]))
    return master_list

# buil "master" taste lists for each artist
taste_list = {}
for person in playlists_collection:
    taste_list[person] = build_master_list(playlists_collection[person])

def plot_taste(taste, type):
    smh = taste.values()
    res = []
    for item in smh :
        res.append(item)
    plt.plot(range(len(taste)), res, type)

def plot_tastes(taste_a, taste_b):
    fig = plt.figure()
    frame = plt.gca()
    
    max_value = 0

    data_a = collections.OrderedDict(songs)
    data_b = collections.OrderedDict(songs)
    data_shared_a = collections.OrderedDict(songs)
    data_shared_b = collections.OrderedDict(songs)

    for song in data_a:
        data_a[song] = np.nan
        data_b[song] = np.nan
        data_shared_a[song] = np.nan
        data_shared_b[song] = np.nan

    for song in taste_a:
        data_a[song] = taste_a[song]
        max_value = max_value if max_value > taste_a[song] else taste_a[song]

    for song in taste_b:
        data_b[song] = taste_b[song]
        max_value = max_value if max_value > taste_b[song] else taste_b[song]
    
    plot_taste(data_a, 'bo')
    plot_taste(data_b, 'r+')
    
    # find where the two tastes share a song

    shared_taste = {}
    for song in taste_a: 
        if (song in taste_b): 
            shared_taste[song] = taste_a[song]
            data_shared_a[song] = taste_a[song]
            data_shared_b[song] = taste_b[song]

#    plot_taste(data_shared_a, 'go')
#    plot_taste(data_shared_b, 'g+')
    
#    for song in shared_taste:
#        print(song)
#        print(data_a[song])
#        print(data_b[song])
#        print(data_shared_a[song])
#        print(data_shared_b[song])
    
    plt.ylim(ymin = 0)
    plt.ylim(ymax = max_value + 1)
    plt.xlim(xmin = 0)
    plt.xlim(xmax = len(songs))
    frame.xaxis.set_ticks_position('none');
    frame.yaxis.set_ticks_position('left')
    plt.xlabel("songs from MSD")
    plt.ylabel("occurance in the collection")
    plt.title("Occurance of a song in 'our collection' and the 'most similar collection'")
    plt.show()

# figure out how similar taste_b is to tast_a
# returns a number: 0 <= n <= 1
# ie, 1.0 is 100% somilar
# also, even if the two tastes share all the same songs, the song weights (play counts) matter as well, so there is still varience then
def find_similarity(taste_a, taste_b):
    # this is basically the same as dividing them together if they were sparse matrices
    # (i think)
    weights = []
    overlaps = 0
    for song in songs:
        # if song is in one but not the other = 0
        # 
        if ((song in taste_a) and (song in taste_b)):
            a_count = taste_a[song]
            b_count = taste_b[song]
            weight = a_count / b_count if a_count < b_count else b_count / a_count
            weights.append(weight)
            overlaps += 1
        elif ((song in taste_a) or (song in taste_b)):
            weights.append(0)
            
#    print ("overlaps: " + str(overlaps))
    return np.mean(weights)

# make a new taste
#my_taste = build_master_list(build_playlist_set("hip-hop", 0.9, "pop", 0.1))
my_taste = build_master_list(build_playlist_set("hip-hop", 0.5, "pop", 0.5))
#my_taste = build_master_list(build_playlist_set("hip-hop", 0.1, "pop", 0.9))

largest_similarity = 0
most_similar_taste = {}
most_similar_profile = ""
for profile in taste_list:
    similarity = find_similarity(my_taste, taste_list[profile])
#    print ("similarity with '"+ profile +"': " + str(similarity))
    if (similarity > largest_similarity):
        largest_similarity = similarity
        most_similar_taste = taste_list[profile]
        most_similar_profile = profile
print("Most similar profile: " + str(most_similar_profile))
print("Weight: " + str(largest_similarity))
print("")

## Search the most_similar_taste for all the songs NOT in my_taste
recommended_songs = {}
highest_recommended = 0
i = 0
for song in most_similar_taste:
    if (song not in my_taste):
        similarity_weight = most_similar_taste[song]*largest_similarity
        recommended_songs[song] = similarity_weight
#        print("[" + song + "]: " + str(recommended_songs[song]))
        highest_recommended = highest_recommended if highest_recommended > similarity_weight else similarity_weight
        
## find most recommended songs and work our way down

recommend_threshhold = .25
if (recommend_threshhold <= highest_recommended):
    print ("Recommended Songs For You:")
    for song in collections.OrderedDict(sorted(recommended_songs.iteritems(), key=lambda x: x[1], reverse=True)):
        if recommended_songs[song] > .2:
            print("\"" + songs_by_id[song]['name'] + "\" by " + songs_by_id[song]['artist'] + " [weight of {0:.2f}".format(recommended_songs[song]) +"]")
else: 
    print ("No songs to recommend for you (threshhold: " + str(recommend_threshhold) + ")")
                
plot_tastes(my_taste, most_similar_taste)


plt.figure()
plot_taste(recommended_songs, 'r+')
plt.ylim(ymin = 0)
plt.ylim(ymax = highest_recommended + 1)
plt.show()


