# Author: Sai Teja Jammalamadaka
# PGSSP Student : IIIT-Hyderabad
# Roll: 201350905
# Written for the Spring Semester 2015 IRE Course

import xml.sax

class WikiContentHandler(xml.sax.ContentHandler):
    
    def __init__(self):
        xml.sax.ContentHandler.__init__(self)
    
    def startElement(self, name, attrs):
        print("The Start Element = " + name)
    
    def endElement(self, name):
        print("The End Element = " + name)
    
    def characters(self, content):
        print("Characters = " + content)
        

testXMLFile = "sampleXML.xml"
xml.sax.parse(testXMLFile, WikiContentHandler())