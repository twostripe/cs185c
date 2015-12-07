# creates a playlist with songs from the same genre

import	csv
import	sys
import	warnings
import	threading	as	th
from random import randint

import numpy as np

import os

dir = "D:/Mark's Temp Folder/github/cs185c/assignment-05/"
  
songs = np.array(list(csv.reader(open(os.path.join(dir, "songs.csv"), 'rt'))))
header = np.array(list(csv.reader(open(os.path.join(dir, "header.csv"), 'rt'))))

       
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
        
    print("creating '" + genre + "' playlist:")
    
    for the_song in playlist :
        # try and match it to a song in the echonest database
        # but don't try too hard     
            
        print (the_song['id'] + ": " + the_song['name'] + " -- " + the_song['artist'])

    print ("")
    
    return playlist


master_playlist = []
master_playlist.append(build_playlist("hip-hop", 15))
master_playlist.append(build_playlist("hip-hop", 15))
master_playlist.append(build_playlist("hip-hop", 15))
master_playlist.append(build_playlist("hip-hop", 15))
master_playlist.append(build_playlist("hip-hop", 15))
master_playlist.append(build_playlist("hip-hop", 15))
master_playlist.append(build_playlist("hip-hop", 15))
master_playlist.append(build_playlist("hip-hop", 15))
master_playlist.append(build_playlist("hip-hop", 15))
master_playlist.append(build_playlist("hip-hop", 15))
master_playlist.append(build_playlist("hip-hop", 15))
master_playlist.append(build_playlist("hip-hop", 15))
master_playlist.append(build_playlist("hip-hop", 15))
master_playlist.append(build_playlist("hip-hop", 15))
master_playlist.append(build_playlist("hip-hop", 15))
master_playlist.append(build_playlist("hip-hop", 15))
master_playlist.append(build_playlist("hip-hop", 15))
master_playlist.append(build_playlist("hip-hop", 15))
master_playlist.append(build_playlist("hip-hop", 15))

# build "master list"
# mostly to see if we're getting some repeats
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
            
            
            
    for song in master_list: print(song + ", " + str(master_list[song]))
    
build_master_list(master_playlist)
        
