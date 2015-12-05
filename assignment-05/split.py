#import io

songs = open("D:/Mark's Temp Folder/github/cs185c/assignment-05/songs.csv", 'w')
header = open("D:/Mark's Temp Folder/github/cs185c/assignment-05/header.csv", 'w')

i = 0
for line in open("D:/Mark's Temp Folder/github/cs185c/assignment-05/dataset.txt") :
    i = i + 1
    if (i < 10) :
        continue
    if (i == 10) :
        header.write(line)
        continue
    else :
        songs.write(line)

songs.close()
header.close()
