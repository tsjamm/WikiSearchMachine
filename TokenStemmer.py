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

primitive_token_detection = re.compile(u'[^\s]+')
primitive_word_detection = re.compile(u'\A[\w-]+\Z')
primitive_pipe_detection = re.compile(u'\|')

def getStemmedTokens(text):
    content = text.lower()
    #Tokenizing
    tokens = []
    try:
        tokens = nltk.word_tokenize(content)
    except Exception as inst:
        #print type(inst)
        tokens = text.split(" ")
    #Removing StopWords
    tokens1 = []
    for token in tokens:
        if not StopWords.isStopWord(token):
            tokens1.append(token)
    #Stemming
    stemTokens = []
    for token in tokens1:
        if re.match(primitive_word_detection, token):
            stemTokens.append(PorterStemmer().stem_word(token))
        else:
            stemTokens.append(token)
    return stemTokens
    
def getStemmedToken(word):
    token = word.lower()
    if StopWords.isStopWord(token):
        return ""
    if re.match(primitive_word_detection, token):
        return PorterStemmer().stem_word(token)
    else:
        return token