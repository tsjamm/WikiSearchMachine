#!/usr/bin/python
#coding: utf8

# Author: Sai Teja Jammalamadaka
# PGSSP Student : IIIT-Hyderabad
# Roll: 201350905
# Written for the Spring Semester 2015 IRE Course

import nltk
#nltk.download('punkt')   #Needed for word_tokenize
from nltk import PorterStemmer
from nltk import word_tokenize
import re
import StopWords
import gc
import time

primitive_token_detection = re.compile(u'[^\s]+')
primitive_word_detection = re.compile(u'\A[\w-]+\Z')
primitive_pipe_detection = re.compile(u'\|')

profileTime = 0
profileTime1 = 0
profileTime2 = 0
profileTime3 = 0
profileTime4 = 0

#gc.disable()

def getStemmedTokens(text):
    global profileTime,profileTime1,profileTime2,profileTime3,profileTime4
    profileStart = int(round(time.time()*1000))
        #Case-Folding
    lowerText = text.lower()
    profileMiddle1 = int(round(time.time()*1000))
    profileTime += profileMiddle1 - profileStart
        #Only Alphabetic / Alphanumeric characters.....
    content = re.sub(u'[^a-zA-Z0-9]+', ' ', lowerText)
    profileMiddle2 = int(round(time.time()*1000))
    profileTime1 += profileMiddle2 - profileMiddle1
        #Tokenizing
    tokens = []
    #try:
        #tokens = nltk.word_tokenize(content)
    #except Exception as inst:
        ##print type(inst)
    tokens = content.split(" ")
    profileMiddle3 = int(round(time.time()*1000))
    profileTime2 += profileMiddle3 - profileMiddle2
    #Removing StopWords
    tokens1 = []
    for token in tokens:
        if token == "":
            continue
        if not StopWords.isStopWord(token):
            tokens1.append(token)
    profileMiddle4 = int(round(time.time()*1000))
    profileTime3 += profileMiddle4 - profileMiddle3
        #Stemming
    stemTokens = []
    for token in tokens1:
        #if re.match(primitive_word_detection, token):
        #    stemTokens.append(PorterStemmer().stem_word(token))
        #else:
        #    stemTokens.append(token)
        try:
            stemTokens.append(PorterStemmer().stem_word(token))
        except Exception as e:
            #print e
            stemTokens.append(token)
    profileEnd = int(round(time.time()*1000))
    profileTime4 += profileEnd - profileMiddle4
    return stemTokens
    
def getStemmedToken(word):
    token = word.lower()
    if StopWords.isStopWord(token):
        return ""
    if re.match(primitive_word_detection, token):
        return PorterStemmer().stem_word(token)
    else:
        return token