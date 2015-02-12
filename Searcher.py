#!/usr/bin/python
#coding: utf8

# Author: Sai Teja Jammalamadaka
# PGSSP Student : IIIT-Hyderabad
# Roll: 201350905
# Written for the Spring Semester 2015 IRE Course

import QueryHandler
from sys import argv
import Indexer

script, infile = argv

queryObject = QueryHandler.parseQuery("t:The t:magnificent i:movie wonder movie roann")


indexPositionMap = {}
location = 0
with open(infile,"rb") as index_file:
    for line in index_file:
        line_len = len(line)
        parts = line.split('=')
        if len(parts) == 2:
            word = parts[0].lower()
            indexPositionMap[word] = location
            #if word == "roann":
            #    print "{0} has position {1}".format(word,location)
        location += line_len
        
print "count of indexPosMap = {0}".format(len(indexPositionMap))

def checkInIndexPositionMap(term):
    if term in indexPositionMap:
        pos = indexPositionMap[term]
        index_file.seek(pos)
        indexedString = index_file.readline()
        parts = indexedString.split('=')
        if len(parts) == 2:
            word = parts[0]
            ffo = Indexer.getFOFromLine(parts[1])
            return ffo
    return {}

queryFrequencyMap = {}

with open(infile,"rb") as index_file:
    for gT in queryObject["gT"]:
        ffo = checkInIndexPositionMap(gT)
        if len(ffo) > 0:
            toPrint = "{0} is present in : ".format(gT)
            for docID in ffo.keys():
                toPrint += "{0},".format(docID)
            print toPrint
        else:
            print "{0} is Not Found".format(gT)
    for tT in queryObject["tT"]:
        ffo = checkInIndexPositionMap(tT)
        if len(ffo) > 0:
            toPrint = "{0} is present in title of : ".format(tT)
            for docID in ffo.keys():
                if ffo[docID]["t"] > 0:
                    toPrint += "{0},".format(docID)
            print toPrint
        else:
            print "{0} is Not Found in Title".format(tT)
    for bT in queryObject["bT"]:
        ffo = checkInIndexPositionMap(bT)
        if len(ffo) > 0:
            toPrint = "{0} is present in body of : ".format(bT)
            for docID in ffo.keys():
                if ffo[docID]["b"] > 0:
                    toPrint += "{0},".format(docID)
            print toPrint
        else:
            print "{0} is Not Found in Body".format(bT)
    for cT in queryObject["cT"]:
        ffo = checkInIndexPositionMap(cT)
        if len(ffo) > 0:
            toPrint = "{0} is present in Categories of : ".format(cT)
            for docID in ffo.keys():
                if ffo[docID]["c"] > 0:
                    toPrint += "{0},".format(docID)
            print toPrint
        else:
            print "{0} is Not Found in Categories".format(cT)
    for iT in queryObject["iT"]:
        ffo = checkInIndexPositionMap(iT)
        if len(ffo) > 0:
            toPrint = "{0} is present in Infobox of : ".format(iT)
            for docID in ffo.keys():
                if ffo[docID]["i"] > 0:
                    toPrint += "{0},".format(docID)
            print toPrint
        else:
            print "{0} is Not Found in Infobox".format(iT)
        