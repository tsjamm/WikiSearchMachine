#!/usr/bin/python
#coding: utf8

# Author: Sai Teja Jammalamadaka
# PGSSP Student : IIIT-Hyderabad
# Roll: 201350905
# Written for the Spring Semester 2015 IRE Course

import xml
import xml.sax as sax

class WikiContentHandler(sax.ContentHandler):
    
    def __init__(self):
        sax.ContentHandler.__init__(self)
        self.elements = []
        self.current_element = ""
    
    def startElement(self, name, attrs):
        print("The Element Pushed = {0}".format(name))
        self.elements.append(name)
        self.current_element = name
    
    def endElement(self, name):
        print("The Element Popped = {0}".format(name))
        self.elements.pop()
        if self.elements:
            self.current_element = self.elements[len(self.elements)-1]
        else:
            self.current_element = ""
    
    def characters(self, content):
        #unicode_content = unicode(content,"utf-8")
        unicode_content = content.encode("utf-8")
        if unicode_content.strip() and self.current_element:
            print("Characters = {0}".format(unicode_content))

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
sax.parse(testXMLFile, SampleWikiContentHandler())