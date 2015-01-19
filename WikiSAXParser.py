#!/usr/bin/python
#coding: utf8

# Author: Sai Teja Jammalamadaka
# PGSSP Student : IIIT-Hyderabad
# Roll: 201350905
# Written for the Spring Semester 2015 IRE Course

import xml
import xml.sax as sax
import re

primitive_token_detection = re.compile(u'[^\s]+')
primitive_pipe_detection = re.compile(u'\|')
infobox_detection = re.compile(u"{{[\s]*[i|I]nfobox(.*)}}[\s]*'''")

class StopWords(object):
    
    def __init__(self):
        self.stopwords = []
        print("Loading Stopwords from file into memory")
        with open("stopwords.txt") as input_file:
            for input_line_raw in input_file:
                input_line = unicode(input_line_raw,"utf-8")
                input_tokens = input_line.split(', ')
                self.stopwords.extend(input_tokens)
    
    def printStopWordsToTerminal(self):
        for sw in self.stopwords:
            print(sw)

class WikiArticle(object):
    
    def __init__(self):
        self.title = ""
        self.id = ""
        self.revision_id = ""
        self.timestamp = ""
        self.contributer_username = ""
        self.contributer_id = ""
        self.minor = ""
        self.comment = ""
        self.text = ""
        self.infobox = {}
        self.infobox_type = ""
        
    def processArticle(self):
        print("Processing Article: {0}".format(self.title))
        #print("Text = {0}".format(self.text))
        #First need to extract infobox and remove from Text
        self.getInfoBox()
        #need to remove stopwords from the remaining text
        
    def getInfoBox(self):
        match = re.search(infobox_detection, self.text)
        if match:
            infobox_string = match.group(1).strip()
            infobox_tokens = infobox_string.split('|')
            if infobox_tokens:
                if not "=" in infobox_tokens[0]:
                    self.infobox_type = infobox_tokens[0]
                    print("InfoboxType = {0}".format(self.infobox_type))
                for token in infobox_tokens:
                    print token
        

class WikiContentHandler(sax.ContentHandler):
    
    def __init__(self):
        sax.ContentHandler.__init__(self)
        self.elements = []
        self.parent_element = ""
        self.current_element = ""
        self.current_article = {}
        self.current_characters = ""
    
    def startElement(self, name, attrs):
        #print("The Element Pushed = {0}".format(name))
        self.elements.append(name)
        if self.current_element:
            self.parent_element = self.current_element
        self.current_element = name
        self.current_characters = ""
        if name == "page":
            self.current_article = WikiArticle()
    
    def endElement(self, name):
        if name == "page":
            self.current_article.processArticle()
        to_store = self.current_characters.strip()
        if name == "title":
            self.current_article.title = to_store
        if name == "id":
            if self.parent_element == "page":
                self.current_article.id = to_store
            if self.parent_element == "revision":
                self.current_article.revision_id = to_store
            if self.parent_element == "contributer":
                self.current_article.contributer_id = to_store
        if name == "timestamp":
            self.current_article.timestamp = to_store
        if name == "username":
            self.current_article.contributer_username = to_store
        if name == "minor":
            self.current_article.minor = to_store
        if name == "comment":
            self.current_article.comment = to_store
        if name == "text":
            self.current_article.text = to_store
                
        #print("The Element Popped = {0}".format(name))
        self.elements.pop()
        if self.elements:
            self.current_element = self.parent_element
            if len(self.elements) == 1:
                self.parent_element = ""
            else:
                self.parent_element = self.elements[len(self.elements)-1]
        else:
            self.current_element = ""
    
    def characters(self, content):
        #unicode_content = unicode(content,"utf-8")
        unicode_content = content.encode("utf-8").strip()
        if unicode_content and self.current_element:
            #print("Characters = {0}".format(unicode_content))
            self.current_characters += unicode_content + " "
        


s_w = StopWords()
sax.parse("sampleXML.xml", WikiContentHandler())

