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

indexPositionMap = {}
def getIndexPositionMap():
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

docIDTitleMap = {}
def getdocIDTitleMap():
    with open(infile+".titles","r") as titles_file:
        for line in titles_file:
            parts = line.split('=')
            if len(parts) == 2:
                id = parts[0]
                title = parts[1]
                docIDTitleMap[id] = title
    print "count of docs = {0}".format(len(docIDTitleMap))

def checkInIndexPositionMap(index_file, term):
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

def doSearch(queryObject):
    with open(infile,"rb") as index_file:
        for gT in queryObject["gT"]:
            ffo = checkInIndexPositionMap(index_file, gT)
            if len(ffo) > 0:
                toPrint = "{0} is present in :\n".format(gT)
                for docID in ffo.keys():
                    toPrint += "\t{0}\n".format(docIDTitleMap[docID])
                print toPrint
            else:
                print "{0} is Not Found".format(gT)
        for tT in queryObject["tT"]:
            ffo = checkInIndexPositionMap(index_file, tT)
            if len(ffo) > 0:
                toPrint = "{0} is present in title of :\n".format(tT)
                for docID in ffo.keys():
                    if ffo[docID]["t"] > 0:
                        toPrint += "\t{0}\n".format(docIDTitleMap[docID])
                print toPrint
            else:
                print "{0} is Not Found in Title".format(tT)
        for bT in queryObject["bT"]:
            ffo = checkInIndexPositionMap(index_file, bT)
            if len(ffo) > 0:
                toPrint = "{0} is present in body of :\n".format(bT)
                for docID in ffo.keys():
                    if ffo[docID]["b"] > 0:
                        toPrint += "\t{0}\n".format(docIDTitleMap[docID])
                print toPrint
            else:
                print "{0} is Not Found in Body".format(bT)
        for cT in queryObject["cT"]:
            ffo = checkInIndexPositionMap(index_file, cT)
            if len(ffo) > 0:
                toPrint = "{0} is present in Categories of :\n".format(cT)
                for docID in ffo.keys():
                    if ffo[docID]["c"] > 0:
                        toPrint += "\t{0}\n".format(docIDTitleMap[docID])
                print toPrint
            else:
                print "{0} is Not Found in Categories".format(cT)
        for iT in queryObject["iT"]:
            ffo = checkInIndexPositionMap(index_file, iT)
            if len(ffo) > 0:
                toPrint = "{0} is present in Infobox of :\n".format(iT)
                for docID in ffo.keys():
                    if ffo[docID]["i"] > 0:
                        toPrint += "\t{0}\n".format(docIDTitleMap[docID])
                print toPrint
            else:
                print "{0} is Not Found in Infobox".format(iT)

getIndexPositionMap()
getdocIDTitleMap()
queryObject = QueryHandler.parseQuery("t:The t:magnificent i:movie roann")
doSearch(queryObject)