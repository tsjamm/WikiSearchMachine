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

script, infile, outfile = argv

start = int(round(time.time()*1000))

Indexer.doInit(outfile)

if infile.endswith(".bz2"):
    with bz2.BZ2File(infile, 'rb', compresslevel=9) as compressed_infile:
        sax.parse(compressed_infile, WikiContentHandler(outfile))
else:
    sax.parse(infile, WikiContentHandler(outfile))

#Indexer.mergeWriter(outfile) #This writes to outfile.... this one is bad... 
Indexer.linearWriter(outfile) #This one is good. :)
Indexer.linearMerger(outfile)
Indexer.writeIndexPartFiles(outfile)
Indexer.writeDocIdTitlesToFile(outfile)

end = int(round(time.time()*1000))

with open(outfile+".done","w") as done_file:
    toPrint = "Process is complete. Time Taken in milliseconds = {0}".format((end-start))
    print toPrint
    done_file.write(toPrint)
