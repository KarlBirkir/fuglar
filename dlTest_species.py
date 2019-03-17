#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 17:40:57 2019

@author: KarlBirkir
This is some pretty nasty looking code in some places, 
but I hope it's useful and saves you some minutes.

"""

import urllib.request, json, math

#countries = ["iceland", "norway", "france"]
species = ["apricaria", "phaeopus", "gallinago", "paradisea", "cygnus", "anser", "corax",
           "vulgaris", "iliacus", "alba", "fuscus", "ostralegus"]
# nums of mp3s to dl per country, leave 0 for all available, try 10 or 15 to test
numDls = 0 
# rate of print messages during dl            
alertRate = 50

#%%
for specie in species: 
    #print("Fetching data on specie: " + specie)
    server = "https://www.xeno-canto.org/api/2/recordings?query="
    countryUrl = server + specie
    
    recordings = []
  
        # Checks to see if there are more than one page 
    with urllib.request.urlopen(countryUrl) as url:
        data = json.loads(url.read().decode())
        numRecordings = data['numRecordings']
        numPages = math.ceil(int(data['numRecordings']) / 500)
            
        print("number of available recordings of " + specie + " : %d " % int(data['numRecordings']))
    del(data)   

#%%
    
    pageUrl = "&page="
    
        # Makes a list of recordings over available pages
    for page in range(1,numPages+1):
        spUrl = server + specie + pageUrl + str(page)
        dataBuf = json.loads(urllib.request.urlopen(countryUrl).read().decode())
        recordings += dataBuf['recordings']
    
    del(dataBuf)

    
    names=[]
    filePaths=[]     # dl paths, links to mp3's
    file_names = []    
    
    for i in range(len(recordings)):
        names.append(recordings[i]["en"])
        filePaths.append("http:" + recordings[i]["file"])
        
        filenameStart = filePaths[i].find("/", 23)+1                             
        filenameEnd = filePaths[i].find("/", 28)
        file_names.append(filePaths[i][filenameStart:filenameEnd])
        
        
#    print("number of recordings downloaded from " + country + " : " + str(len(recordings)))
#    print("number of names: " + str(len(names)))
    print("number of possible files to download: " + str(len(filePaths)))
    if(numDls != 0):
        print("but only downloading : " + str(numDls))

#%%
        #download files
    if(numDls == 0):
        numDls = len(recordings)

    for dlUrl in range(0,numDls):
        if(dlUrl % alertRate == 0):
            print("downloading nr : " + str(dlUrl))
        usock = urllib.request.urlopen(filePaths[dlUrl])                                  
        f = open(file_names[dlUrl] + ".mp3", 'wb')
        downloaded = 0
        block_size = 8192                                            
        while True:
            buff = usock.read(block_size)
            if not buff:
                break
            f.write(buff)
        f.close()

print("Finished")

#%%

# nameFileDict = zip(names, )