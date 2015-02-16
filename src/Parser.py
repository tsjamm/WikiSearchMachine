#!/usr/bin/python
#coding: utf8

# Author: Sai Teja Jammalamadaka
# PGSSP Student : IIIT-Hyderabad
# Roll: 201350905
# Written for the Spring Semester 2015 IRE Course

import xml
import xml.sax as sax
import re
from StringIO import StringIO
from sys import argv

from shutil import copyfileobj
import bz2
import time

import Indexer
from WikiSAXHandler import WikiContentHandler
import TokenStemmer

script, infile, outfile = argv

toPrintProfile = ""    

start = int(round(time.time()*1000))

Indexer.doInit(outfile)

profileStart = int(round(time.time()*1000))
if infile.endswith(".bz2"):
    with bz2.BZ2File(infile, 'rb', compresslevel=9) as compressed_infile:
        sax.parse(compressed_infile, WikiContentHandler(outfile))
else:
    sax.parse(infile, WikiContentHandler(outfile))
profileEnd = int(round(time.time()*1000))
toPrintProfile += "sax.parse completed. Time Taken in milliseconds = {0}\n".format((profileEnd-profileStart))

toPrintProfile += "Index.profileTime in milliseconds = {0}\n".format(Indexer.profileTime)
toPrintProfile += "Index.profileTime1 in milliseconds = {0}\n".format(Indexer.profileTime1)
toPrintProfile += "Index.profileTime2 in milliseconds = {0}\n".format(Indexer.profileTime2)
toPrintProfile += "Index.profileTime3 in milliseconds = {0}\n".format(Indexer.profileTime3)
toPrintProfile += "Index.profileTime4 in milliseconds = {0}\n".format(Indexer.profileTime4)

toPrintProfile += "TokenStemmer.profileTime in milliseconds = {0}\n".format(TokenStemmer.profileTime)
toPrintProfile += "TokenStemmer.profileTime1 in milliseconds = {0}\n".format(TokenStemmer.profileTime1)
toPrintProfile += "TokenStemmer.profileTime2 in milliseconds = {0}\n".format(TokenStemmer.profileTime2)
toPrintProfile += "TokenStemmer.profileTime3 in milliseconds = {0}\n".format(TokenStemmer.profileTime3)
toPrintProfile += "TokenStemmer.profileTime4 in milliseconds = {0}\n".format(TokenStemmer.profileTime4)


#Indexer.mergeWriter(outfile) #This writes to outfile.... this one is bad... 
profileStart = int(round(time.time()*1000))
Indexer.linearWriter(outfile) #This one is good. :)
profileEnd = int(round(time.time()*1000))
toPrintProfile += "Indexer.linearWriter completed. Time Taken in milliseconds = {0}\n".format((profileEnd-profileStart))

profileStart = int(round(time.time()*1000))
Indexer.linearMerger(outfile)
profileEnd = int(round(time.time()*1000))
toPrintProfile += "Indexer.linearMerger completed. Time Taken in milliseconds = {0}\n".format((profileEnd-profileStart))

profileStart = int(round(time.time()*1000))
Indexer.writeIndexPartFiles(outfile)
profileEnd = int(round(time.time()*1000))
toPrintProfile += "Indexer.writeIndexPartFiles completed. Time Taken in milliseconds = {0}\n".format((profileEnd-profileStart))

# profileStart = int(round(time.time()*1000))
# Indexer.writeDocIdTitlesToFile(outfile)
# profileEnd = int(round(time.time()*1000))
# toPrintProfile += "Indexer.writeDocIdTitlesToFile completed. Time Taken in milliseconds = {0}\n".format((profileEnd-profileStart))

end = int(round(time.time()*1000))

with open(outfile+".parser.done","w") as done_file:
    toPrintProfile += "Process is complete. Time Taken in milliseconds = {0}\n".format((end-start))
    print toPrintProfile
    done_file.write(toPrintProfile)
