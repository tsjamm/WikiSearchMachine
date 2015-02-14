#!/usr/bin/python
#coding: utf8

# Author: Sai Teja Jammalamadaka
# PGSSP Student : IIIT-Hyderabad
# Roll: 201350905
# Written for the Spring Semester 2015 IRE Course

import re
import TokenStemmer
import os.path

TermFreqMap = {}
DocumentIDTitleMap = {}
freq_string_detection = re.compile("([0-9]*)t([0-9]*)b([0-9]*)c([0-9]*)i([0-9]*)")
articleCount = 0
toDumpCount = 0

def doInit(outfile):
    if not os.path.exists(outfile):
        out_file = open(outfile,"w")
        out_file.close()
    if not os.path.exists(outfile+".tmp"):
        temp_file = open(outfile+".tmp","w")
        temp_file.close()


def doIndex(wikiArticle, outfile):
    global articleCount
    global toDumpCount
    articleCount += 1
    toDumpCount += 1
    DocumentIDTitleMap[wikiArticle.id] = wikiArticle.title
    buildTermFreqMap(wikiArticle)
    checkTermFreqMapSizeAndWrite(outfile)

def buildTermFreqMap(wikiArticle):
    title_tokens = TokenStemmer.getStemmedTokens(wikiArticle.title)
    for token in title_tokens:
        putTitleTokenInTermFreqMap(token, wikiArticle.id)
    #link_tokens = wikiArticle.external_links
    #for token in link_tokens:
    #    putTokenInTermFreqMap(token)
    cat_tokens = TokenStemmer.getStemmedTokens(getStringFromListofStrings(wikiArticle.categories))
    for token in cat_tokens:
        putCatTokenInTermFreqMap(token, wikiArticle.id)
    ib_tokens = TokenStemmer.getStemmedTokens(wikiArticle.infobox_values_string)
    for token in ib_tokens:
        putIBTokenInTermFreqMap(token, wikiArticle.id)
    text_tokens = TokenStemmer.getStemmedTokens(wikiArticle.text)
    for token in text_tokens:
        putBodyTokenInTermFreqMap(token, wikiArticle.id)

def checkTermFreqMapSizeAndWrite(outfile):
    #if len(TermFreqMap) > 10000:
        #IndexWriter().mergeWriter()
    global toDumpCount
    if toDumpCount >= 2000:
        mergeWriter(outfile)
        #linearWriter(outfile)
        toDumpCount = 0
        

def checkIfTokenInTermFreqMap(token, wAid):
    
    if token not in TermFreqMap:
        freq_obj = {}
        TermFreqMap[token] = freq_obj
    if wAid not in TermFreqMap[token]:
        freq_doc_obj = {}
        freq_doc_obj["t"] = 0 #title
        freq_doc_obj["b"] = 0 #body
        freq_doc_obj["c"] = 0 #cat
        freq_doc_obj["i"] = 0 #infobox
        TermFreqMap[token][wAid] = freq_doc_obj

def putTitleTokenInTermFreqMap(token,wAid):
    checkIfTokenInTermFreqMap(token,wAid)
    TermFreqMap[token][wAid]["t"] += 1
    
def putBodyTokenInTermFreqMap(token,wAid):
    checkIfTokenInTermFreqMap(token,wAid)
    TermFreqMap[token][wAid]["b"] += 1
    
def putCatTokenInTermFreqMap(token,wAid):
    checkIfTokenInTermFreqMap(token,wAid)
    TermFreqMap[token][wAid]["c"] += 1
    
def putIBTokenInTermFreqMap(token,wAid):
    checkIfTokenInTermFreqMap(token,wAid)
    TermFreqMap[token][wAid]["i"] += 1

def getStringFromListofStrings(list):
    toReturn = ""
    for str in list:
        toReturn += str + " "
    return toReturn
        

        
# HERE STARTS THE WRITER PART.....
        
def getFOFromLine(fline):
    freq_obj = {}
    docs = fline.split(';')
    # print docs
    for doc in docs:
        # print doc
        parts = doc.split(':')
        if len(parts) != 2:
            continue
        # print parts
        did = parts[0]
        # print did
        fstring = parts[1]
        freq_doc_obj = {}
        
        matches = re.finditer(freq_string_detection, fstring)
        if matches:
            for match in matches:
                total = 0
                total_match = match.group(1)
                if total_match != "":
                    total = int(total_match)
                title = 0
                title_match = match.group(2)
                if title_match != "":
                    title = int(title_match)
                body = 0
                body_match = match.group(3)
                if body_match != "":
                    body = int(body_match)
                cat = 0
                cat_match = match.group(4)
                if cat_match != "":
                    cat = int(cat_match)
                infob = 0
                infob_match = match.group(5)
                if infob_match != "":
                    infob = int(infob_match)
                freq_doc_obj["t"] = title #title
                freq_doc_obj["b"] = body #body
                freq_doc_obj["c"] = cat #cat
                freq_doc_obj["i"] = infob #infobox
        freq_obj[did] = freq_doc_obj
    return freq_obj

def getNewFO(word, ffo):
    if word in TermFreqMap:
        mfo = TermFreqMap[word]
        cfo = dict(mfo.items() + ffo.items())
        return cfo
    else:
        return ffo

def removeMFO(word):
    if word in TermFreqMap:
        del TermFreqMap[word]

linearWriterCount = 0
def linearWriter(outfile):
    global linearWriterCount
    linearWriterCount += 1
    with open("{0}.tmp{1}".format(outfile,linearWriterCount),"w") as temp_file:
        for word in TermFreqMap:
            fo = TermFreqMap[word]
            toWrite = u"" + word + "=" + getFOString(fo)
            temp_file.write(toWrite.encode('utf-8'))
        TermFreqMap.clear()
    print("tempfile {0} created :::: Article Count = {1}".format(linearWriterCount,articleCount))
'''
def linearMerger(outfile):
    global linearWriterCount
    with open(outfile+".tmp","w") as temp_file:
        for i in xrange(1,linearWriterCount+1):
            with open("{0}.tmp{1}".format(outfile,i),"r") as old_file:
                for line in old_file:
                    parts = line.split('=')
                    if len(parts) == 2:
                        word = parts[0]
                        ffo = getFOFromLine(parts[1])
                        cfo = getNewFO(word, ffo)
                        removeMFO(word)
                        toWrite = u"" + word + "=" + getFOString(cfo)
                        temp_file.write(toWrite.encode('utf-8'))
'''        
def mergeWriter(outfile):
    with open(outfile+".tmp","w") as temp_file:
        with open(outfile,"r") as old_file:
            for line in old_file:
                parts = line.split('=')
                if len(parts) == 2:
                    word = parts[0]
                    ffo = getFOFromLine(parts[1])
                    cfo = getNewFO(word, ffo)
                    removeMFO(word)
                    toWrite = u"" + word + "=" + getFOString(cfo)
                    temp_file.write(toWrite.encode('utf-8'))
        for word in TermFreqMap:
            fo = TermFreqMap[word]
            toWrite = u"" + word + "=" + getFOString(fo)
            temp_file.write(toWrite.encode('utf-8'))
        TermFreqMap.clear()
    
    with open(outfile+".tmp","r") as temp_file:
        with open(outfile,"w") as new_file:
            for line in temp_file:
                new_file.write(line)
    
    with open(outfile+".tmp","w") as temp_file:
        print("tempfile copied and erased :::: Article Count = {0}".format(articleCount))

def getFOString(fo):
    toWrite = u""
    for did in fo:
        toWrite += did+":"
        fdo = fo[did]
        tfreq = fdo["t"]
        bfreq = fdo["b"]
        cfreq = fdo["c"]
        ifreq = fdo["i"]
        total_freq = tfreq+bfreq+cfreq+ifreq
        if total_freq != 0 :
            toWrite += "{0}".format(total_freq)
        toWrite += "t"
        if tfreq != 0 :
            toWrite += "{0}".format(tfreq)
        toWrite += "b"
        if bfreq != 0 :
            toWrite += "{0}".format(bfreq)
        toWrite += "c"
        if cfreq != 0 :
            toWrite += "{0}".format(cfreq)
        toWrite += "i"
        if ifreq != 0 :
            toWrite += "{0}".format(ifreq)
        toWrite += ";"
        #toWrite += "{0}t{1}b{2}c{3}i{4};".format(total_freq,tfreq,bfreq,cfreq,ifreq)
    toWrite += "\n"
    return toWrite
        
def writeDocIdTitlesToFile(outfile):
    with open(outfile+".titles","w") as titles_file:
        for docid in DocumentIDTitleMap.keys():
            titles_file.write("{0}={1}\n".format(docid,DocumentIDTitleMap[docid]))