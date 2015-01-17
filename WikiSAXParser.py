#!/usr/bin/python
#coding: utf8

# Author: Sai Teja Jammalamadaka
# PGSSP Student : IIIT-Hyderabad
# Roll: 201350905
# Written for the Spring Semester 2015 IRE Course

import xml
import xml.sax as sax

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
        
    def processArticle(self):
        print("Processing Article: {0}".format(self.title))
        

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
            print(self.current_article.title)
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

# This class is just a sample one that prints stuff to the terminal for testing purposes
class SampleWikiContentHandler(sax.ContentHandler):
    
    def __init__(self):
        sax.ContentHandler.__init__(self)
        self.elements = []
        self.current_element = ""
    
    def startElement(self, name, attrs):
        #print("The Element Pushed = {0}".format(name))
        self.elements.append(name)
        self.current_element = name
        toPrint = ""
        for i in range(len(self.elements)):
            toPrint += "    "
        toPrint += self.current_element
        print(toPrint)
    
    def endElement(self, name):
        toPrint = ""
        for i in range(len(self.elements)):
            toPrint += "    "
        toPrint += "/" + self.current_element
        print(toPrint)
        #print("The Element Popped = {0}".format(name))
        self.elements.pop()
        if self.elements:
            self.current_element = self.elements[len(self.elements)-1]
        else:
            self.current_element = ""
    
    def characters(self, content):
        #unicode_content = unicode(content,"utf-8")
        unicode_content = content.encode("utf-8")
        if unicode_content.strip() and self.current_element:
            #print("Characters = {0}".format(unicode_content))
            toPrint = ""
            for i in range(len(self.elements)):
                toPrint += "    "
            toPrint += unicode_content
            #print(toPrint)
        

testXMLFile = "sampleXML.xml"
#sax.parse(testXMLFile, SampleWikiContentHandler())
sax.parse(testXMLFile, WikiContentHandler())