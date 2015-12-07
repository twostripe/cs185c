# creates a playlist with songs from the same genre

import	csv
import	sys
import	warnings
import	threading	as	th
from random import randint
from random import random
import matplotlib.pyplot as plt

import numpy as np

import os

dir = "D:/Mark's Temp Folder/github/cs185c/assignment-05/"
  
songs = np.array(list(csv.reader(open(os.path.join(dir, "songs.csv"), 'rt'))))
#songs = np.array(list(csv.reader(open(os.path.join(dir, "songs_limited.csv"), 'rt'))))
header = np.array(list(csv.reader(open(os.path.join(dir, "header.csv"), 'rt'))))

song_ids = []
for song in songs:
    song_ids.append(song[1])
                 
def build_playlist(genre, num_songs):
    # the genre we're looking for
    # (change this)
    genre_list = []
    
    # put all the songs of a particular genre to one side
    i = 0
    for the_song in songs :
        if the_song[0] == genre :
            genre_list.append({'id': the_song[1], 'name': the_song[3], 'artist': the_song[2]})

    # pick 10 random songs from this list
    playlist = []
    
    i = 0
    for i in range(0,num_songs) :
        playlist.append(genre_list[randint(0,len(genre_list)-1)])
        
#    print("creating '" + genre + "' playlist")
    
    return playlist

# builds a collection of playlists
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
    plt.plot(range(len(taste)), taste.values(), type)

# we can use this "taste" list to see a DJ's taste
plot_taste(taste_list['Alfrig'], 'r+')

# make a new taste
my_taste = build_master_list(build_playlist_set("hip-hop", 0, "pop", 1))
plot_taste(my_taste, 'b+')

# find where the two tastes share a song
shared_taste = {}
for song in my_taste: 
    if (song in taste_list['Alfrig']): 
        shared_taste[song] = my_taste[song]

plot_taste(shared_taste, 'go')

plt.ylim(0, 4)
plt.show()
