#!/usr/bin/python
#coding: utf8

# Author: Sai Teja Jammalamadaka
# PGSSP Student : IIIT-Hyderabad
# Roll: 201350905
# Written for the Spring Semester 2015 IRE Course

from sys import argv
import TokenStemmer

#script, infile, outfile = argv

def parseQuery(queryString):
    tokensObject = {}
    tokensObject["type"] = "union" # Or can be union
    tokensObject["tT"] = [] # title Tokens
    tokensObject["bT"] = [] # bodytext Tokens
    tokensObject["cT"] = [] # category Tokens
    tokensObject["iT"] = [] # infobox Tokens
    tokensObject["gT"] = [] # Genaral Tokens
    queryTokens = queryString.lower().split(" ")
    for qT in queryTokens:
        if qT.startswith("t:"):
            tT = qT.replace("t:","")
            stemmed = TokenStemmer.getStemmedToken(tT)
            if stemmed != "":
                tokensObject["tT"].append(stemmed)
                tokensObject["type"] = "intersection"
            #print "{0} is title query".format(qT)
        elif qT.startswith("b:"):
            bT = qT.replace("b:","")
            stemmed = TokenStemmer.getStemmedToken(bT)
            if stemmed != "":
                tokensObject["bT"].append(stemmed)
                tokensObject["type"] = "intersection"
            #print "{0} is bodytext query".format(qT)
        elif qT.startswith("c:"):
            cT = qT.replace("c:","")
            stemmed = TokenStemmer.getStemmedToken(cT)
            if stemmed != "":
                tokensObject["cT"].append(stemmed)
                tokensObject["type"] = "intersection"
            #print "{0} is category query".format(qT)
        elif qT.startswith("i:"):
            iT = qT.replace("i:","")
            stemmed = TokenStemmer.getStemmedToken(iT)
            if stemmed != "":
                tokensObject["iT"].append(stemmed)
                tokensObject["type"] = "intersection"
            #print "{0} is infobox query".format(qT)
        else:
            stemmed = TokenStemmer.getStemmedToken(qT)
            if stemmed != "":
                tokensObject["gT"].append(stemmed)
                tokensObject["type"] = "intersection"
                #tokensObject["tT"].append(stemmed)
                #tokensObject["bT"].append(stemmed)
                #tokensObject["cT"].append(stemmed)
                #tokensObject["iT"].append(stemmed)
            #print "{0} is general query".format(qT)
            
    #print(tokensObject)
    return tokensObject

#parseQuery("t:this i:is a sample query")