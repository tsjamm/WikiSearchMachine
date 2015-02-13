#!/usr/bin/python
#coding: utf8

# Author: Sai Teja Jammalamadaka
# PGSSP Student : IIIT-Hyderabad
# Roll: 201350905
# Written for the Spring Semester 2015 IRE Course

import QueryHandler
from sys import argv
import operator
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
            
    #print "count of indexPosMap = {0}".format(len(indexPositionMap))

docIDTitleMap = {}
def getdocIDTitleMap():
    with open(infile+".titles","r") as titles_file:
        for line in titles_file:
            parts = line.split('=')
            if len(parts) == 2:
                id = parts[0]
                title = parts[1]
                docIDTitleMap[id] = title
    #print "count of docs = {0}".format(len(docIDTitleMap))
TotalDocNum = len(docIDTitleMap)

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

def intersectLists(lists):
    if len(lists)==0:
        return []
    #start intersecting from the smaller list
    lists.sort(key=len)
    #print lists
    new_lists = []
    for l in lists:
        if len(l) != 0:
            new_lists.append(l)
    #print new_lists
    return list(reduce(lambda x,y: set(x)&set(y),new_lists))

def getSortedTuples(freq_map):
    sorted_tuples = sorted(freq_map.iteritems(), key=operator.itemgetter(1))
    return sorted_tuples
    
def doSearch(queryObject, numOfResults):
    queryDocList = []
    #ffoMap = {}
    with open(infile,"rb") as index_file:
        gTqueryDocList = {}
        for gT in queryObject["gT"]:
            ffo = checkInIndexPositionMap(index_file, gT)
            if len(ffo) > 0:
                #ffoMap[gT] = ffo
                DF = len(ffo.keys())
                IDF = TotalDocNum / DF
                for docID in ffo.keys():
                    TF = ffo[docID]["t"] + ffo[docID]["b"] + ffo[docID]["c"] + ffo[docID]["i"]
                    gTqueryDocList[docID] = TF * IDF
        tTqueryDocList = {}
        for tT in queryObject["tT"]:
            ffo = checkInIndexPositionMap(index_file, tT)
            if len(ffo) > 0:
                #ffoMap[tT] = ffo
                DF = len(ffo.keys())
                IDF = TotalDocNum / DF
                for docID in ffo.keys():
                    if ffo[docID]["t"] > 0:
                        TF = ffo[docID]["t"]
                        tTqueryDocList[docID] = TF * IDF
        bTqueryDocList = {}
        for bT in queryObject["bT"]:
            ffo = checkInIndexPositionMap(index_file, bT)
            if len(ffo) > 0:
                #ffoMap[bT] = ffo
                DF = len(ffo.keys())
                IDF = TotalDocNum / DF
                for docID in ffo.keys():
                    if ffo[docID]["b"] > 0:
                        TF = ffo[docID]["b"]
                        bTqueryDocList[docID] = TF * IDF
        cTqueryDocList = {}
        for cT in queryObject["cT"]:
            ffo = checkInIndexPositionMap(index_file, cT)
            if len(ffo) > 0:
                #ffoMap[cT] = ffo
                DF = len(ffo.keys())
                IDF = TotalDocNum / DF
                for docID in ffo.keys():
                    if ffo[docID]["c"] > 0:
                        TF = ffo[docID]["c"]
                        cTqueryDocList[docID] = TF * IDF
        iTqueryDocList = {}
        for iT in queryObject["iT"]:
            ffo = checkInIndexPositionMap(index_file, iT)
            if len(ffo) > 0:
                #ffoMap[iT] = ffo
                DF = len(ffo.keys())
                IDF = TotalDocNum / DF
                for docID in ffo.keys():
                    if ffo[docID]["i"] > 0:
                        TF = ffo[docID]["i"]
                        iTqueryDocList[docID] = TF * IDF
        
        tfidfDOCMap = {}
        
        if queryObject["type"] == "intersection":
            #print "Doing Intersection Query"
            #queryDocList = list(set(iTqueryDocList.keys()) & set(cTqueryDocList.keys()) & set(bTqueryDocList.keys()) & set(tTqueryDocList.keys()) & set(gTqueryDocList.keys()))
            toIntersect = [iTqueryDocList.keys(),cTqueryDocList.keys(),bTqueryDocList.keys(),tTqueryDocList.keys(),gTqueryDocList.keys()]
            queryDocList = intersectLists(toIntersect)
            for doc in queryDocList:
                TFIDF = 0
                if doc in iTqueryDocList:
                    TFIDF += iTqueryDocList[doc]*0.4
                if doc in cTqueryDocList:
                    TFIDF += cTqueryDocList[doc]*0.4
                if doc in bTqueryDocList:
                    TFIDF += bTqueryDocList[doc]*0.2
                if doc in tTqueryDocList:
                    TFIDF += tTqueryDocList[doc]*0.8
                if doc in gTqueryDocList:
                    TFIDF += gTqueryDocList[doc]*0.4
                tfidfDOCMap[doc] = TFIDF
        else:
            #print "Doing Regular Query"
            queryDocList.extend(gTqueryDocList.keys())
            for doc in queryDocList:
                TFIDF = 0
                if doc in gTqueryDocList:
                    TFIDF = gTqueryDocList[doc]
                tfidfDOCMap[doc] = TFIDF
        
        sorted_tuples = getSortedTuples(tfidfDOCMap)
        sorted_tuples.reverse()
        toReturnList = []
        topNtuples = sorted_tuples[:numOfResults]
        for pair in topNtuples:
            toReturnList.append(pair[0])
        return toReturnList
    return []


getIndexPositionMap()
getdocIDTitleMap()
queryObject = QueryHandler.parseQuery("t:roann")
listOfDocIDs = doSearch(queryObject,10)

for doc in listOfDocIDs:
    print docIDTitleMap[doc]