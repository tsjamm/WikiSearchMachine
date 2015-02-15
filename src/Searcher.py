#!/usr/bin/python
#coding: utf8

# Author: Sai Teja Jammalamadaka
# PGSSP Student : IIIT-Hyderabad
# Roll: 201350905
# Written for the Spring Semester 2015 IRE Course

import QueryHandler
import sys
from sys import argv
import operator
import Indexer
import bisect
import bz2
import time

script, infile = argv

TotalDocNum = 0
docIDTitleMap = {}
def getdocIDTitleMap():
    global TotalDocNum
    with open(infile+".titles","r") as titles_file:
        for line in titles_file:
            parts = line.strip().split('=')
            if len(parts) == 2:
                id = parts[0]
                title = parts[1]
                docIDTitleMap[id] = title
    #print "count of docs = {0}".format(len(docIDTitleMap))
    TotalDocNum = len(docIDTitleMap)
    #print "TotalDocNum = {0}".format(TotalDocNum)

indexFileCount = 0
indexFileWordMap = {}
def getIndexFileWordMap():
    global indexFileCount
    with open(infile+".indexWordMap","r") as temp_file:
        for line in temp_file:
            parts = line.strip().split('=')
            if len(parts) == 2:
                index = parts[1]
                word = parts[0]
                indexFileWordMap[index] = word
    indexFileCount = len(indexFileWordMap)


def checkInIndexFileWordMap(term):
    #print "term is {0}".format(term)
    sortedKeys = sorted(indexFileWordMap.keys())
    #print "sortedKeys = {0}".format(sortedKeys)
    pos = bisect.bisect(sortedKeys,term)
    if pos > 0:
        pos = pos - 1
    key = sortedKeys[pos]
    index = indexFileWordMap[key]
    #print "key = {0} and index = {1}".format(key,index)
    with bz2.BZ2File("{0}.index{1}.bz2".format(infile,index), 'rb', compresslevel=9) as ipartF:
        #print "checking file {0}.index{1}.bz2".format(infile,index)
        for line in ipartF:
            if line.startswith(term):
                parts = line.strip().split("=")
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
    if len(new_lists)==0:
        return []
    return list(reduce(lambda x,y: set(x)&set(y),new_lists))

def getSortedTuples(freq_map):
    sorted_tuples = sorted(freq_map.iteritems(), key=operator.itemgetter(1))
    return sorted_tuples
    
def doSearch(queryObject, numOfResults):
    queryDocList = []
    #ffoMap = {}
    gTqueryDocList = {}
    for gT in queryObject["gT"]:
        ffo = checkInIndexFileWordMap(gT)
        if len(ffo) > 0:
            #ffoMap[gT] = ffo
            DF = len(ffo.keys())
            IDF = TotalDocNum / DF
            for docID in ffo.keys():
                TF = ffo[docID]["t"] + ffo[docID]["b"] + ffo[docID]["c"] + ffo[docID]["i"]
                gTqueryDocList[docID] = TF * IDF
    tTqueryDocList = {}
    for tT in queryObject["tT"]:
        ffo = checkInIndexFileWordMap(tT)
        #print "tT = {0}, ffo = {1}".format(tT,ffo)
        if len(ffo) > 0:
            #ffoMap[tT] = ffo
            DF = len(ffo.keys())
            IDF = TotalDocNum / DF
            for docID in ffo.keys():
                if ffo[docID]["t"] > 0:
                    TF = ffo[docID]["t"]
                    tTqueryDocList[docID] = TF * IDF
        #print "tTqueryDocList = {0}".format(tTqueryDocList)
    bTqueryDocList = {}
    for bT in queryObject["bT"]:
        ffo = checkInIndexFileWordMap(bT)
        #print "bT = {0}, ffo = {1}".format(bT,ffo)
        if len(ffo) > 0:
            #ffoMap[bT] = ffo
            DF = len(ffo.keys())
            IDF = TotalDocNum / DF
            #print "DF = {0} IDF = {1} TotalDocNum = {2}".format(DF,IDF,TotalDocNum)
            for docID in ffo.keys():
                if ffo[docID]["b"] > 0:
                    TF = ffo[docID]["b"]
                    bTqueryDocList[docID] = TF * IDF
        #print "bTqueryDocList = {0}".format(bTqueryDocList)
    cTqueryDocList = {}
    for cT in queryObject["cT"]:
        ffo = checkInIndexFileWordMap(cT)
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
        ffo = checkInIndexFileWordMap(iT)
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
                TFIDF += cTqueryDocList[doc]*0.6
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
    #print sorted_tuples
    sorted_tuples.reverse()
    #print sorted_tuples
    toReturnList = []
    topNtuples = sorted_tuples[:numOfResults]
    for pair in topNtuples:
        toReturnList.append(pair[0])
    #print toReturnList
    return toReturnList
    # return []


start = int(round(time.time()*1000))

#getIndexPositionMap()
getIndexFileWordMap()
getdocIDTitleMap()



f = sys.stdin
queries =  []
for line in f.readlines():
    queries.append(line.strip())
queryNo = int(queries[0])
queries = queries[1:]

for query in queries:
    queryObject = QueryHandler.parseQuery(query)
    listOfDocIDs = doSearch(queryObject,10)
    print "Query = {0}".format(query)
    for doc in listOfDocIDs:
        print docIDTitleMap[doc]
    print ""
    
end = int(round(time.time()*1000))
with open(infile+".doneSearch","w") as done_file:
    toPrint = "Process is complete. Time Taken in milliseconds = {0}".format((end-start))
    print toPrint
    done_file.write(toPrint)