# creates a playlist with songs from the same genre

import	csv
import	sys
import	warnings
import	numpy		as	np
import	threading	as	th
from random import randint


songs = np.array(list(csv.reader(open("D:/Mark's Temp Folder/github/cs185c/assignment-05/songs.csv", 'rt'))))
header = np.array(list(csv.reader(open("D:/Mark's Temp Folder/github/cs185c/assignment-05/header.csv", 'rt'))))

# the genre we're looking for
# (change this)
genre = "jazz and blues"
genre_list = []

# put all the songs of a particular genre to one side
i = 0
for song in songs :
    if song[0] == genre :
        genre_list.append({'id': song[1], 'name': song[3], 'artist': song[2]})
       
# pick 10 random songs from this list
playlist = []

i = 0
for i in range(0,10) :
    playlist.append(genre_list[randint(0,len(genre_list)-1)])
    
for song in playlist :
    print song['name'] + " -- " + song['artist']
