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
#sax.parse("sampleXML.xml", WikiContentHandler())
sax.parse(infile, WikiContentHandler(outfile))
Indexer.mergeWriter(outfile) #This writes to outfile....
Indexer.writeDocIdTitlesToFile(outfile)


with open(outfile+".sorted","w") as sorted_file:
    with open(outfile,"r") as unsorted_file:
        for line in sorted(unsorted_file, key = str.lower):
            sorted_file.write(line)

with open(outfile+".sorted", 'rb') as toCompress:
    with bz2.BZ2File(outfile+".bz2", 'wb', compresslevel=9) as compressed:
        copyfileobj(toCompress, compressed)

end = int(round(time.time()*1000))

with open(outfile+".done","w") as done_file:
    toPrint = "Process is complete. Time Taken in milliseconds = {0}".format((end-start))
    print toPrint
    done_file.write(toPrint)
