# Author: Sai Teja Jammalamadaka
# PGSSP Student : IIIT-Hyderabad
# Roll: 201350905
# Written for the Spring Semester 2015 IRE Course

#coding: utf8

import xml.sax

class WikiContentHandler(xml.sax.ContentHandler):
    
    def __init__(self):
        xml.sax.ContentHandler.__init__(self)
    
    def startElement(self, name, attrs):
        print("The Start Element = {0}".format(name))
    
    def endElement(self, name):
        print("The End Element = {0}".format(name))
    
    def characters(self, content):
        #unicode_content = unicode(content,"utf-8")
        unicode_content = content.encode("utf-8")
        if unicode_content.strip():
            print("Characters = {0}".format(unicode_content))
        

testXMLFile = "sampleXML.xml"
xml.sax.parse(testXMLFile, WikiContentHandler())