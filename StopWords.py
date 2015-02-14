#!/usr/bin/python
#coding: utf8

# Author: Sai Teja Jammalamadaka
# PGSSP Student : IIIT-Hyderabad
# Roll: 201350905
# Written for the Spring Semester 2015 IRE Course

StopWordsList = []    

#print("Loading Stopwords from file into memory")
with open("stopwords.txt") as input_file:
    for input_line_raw in input_file:
        # print type(input_line_raw)
        input_line = unicode(input_line_raw,"utf-8")
        # print type(input_line)
        input_tokens = input_line_raw.split(', ')
        StopWordsList.extend(input_tokens)

def isStopWord(token):
    if token in StopWordsList:
        return True
    else: 
        return False

def printStopWordsToTerminal():
    for sw in StopWordsList:
        print(sw)