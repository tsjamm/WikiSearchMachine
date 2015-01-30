#!/usr/bin/python
#coding: utf8

# Author: Sai Teja Jammalamadaka
# PGSSP Student : IIIT-Hyderabad
# Roll: 201350905
# Written for the Spring Semester 2015 IRE Course

import xml
import xml.sax as sax
import re
from StringIO import StringIO
from sys import argv
import nltk
nltk.download('punkt')   #Needed for word_tokenize
from nltk import PorterStemmer
from nltk import word_tokenize

script, infile, outfile = argv

primitive_token_detection = re.compile(u'[^\s]+')
primitive_word_detection = re.compile(u'\A[\w-]+\Z')
primitive_pipe_detection = re.compile(u'\|')
# Infobox Detection does not work with this regext due to misplaced infoboxes
#infobox_detection = re.compile(u"{{[\s]*infobox(.*)}}[\s]*'''",re.I)
INFOBOX_START_STRING = u"{{Infobox"
infobox_start_detection = re.compile(INFOBOX_START_STRING,re.I)
CITE_START_STRING = u"{{cite"
cite_start_detection = re.compile(CITE_START_STRING,re.I)

external_links_detection = re.compile(u"http[^\s]+\s",re.I|re.M)
flower_detection = re.compile("{{(.*?)}}");

redirect_detection = re.compile(u"#REDIRECT\s?\[\[(.*?)\]\]",re.I)
stub_detection = re.compile(u"-stub}}")
disambig_detection = re.compile(u"{{disambig}}")
category_detection = re.compile(u"\[\[Category:(.*?)\]\]",re.M)
link_detection = re.compile(u"\[\[(.*?)\]\]",re.M)
relations_detection = re.compile(u"\[\[([^\[\]]+)\]\]",re.M|re.S)
section_detection = re.compile(u"^==([^=].*?[^=])==$",re.M)
sub_section_detection =re.compile(u"^===([^=].*?[^=])===$",re.M)

TermFreqMap = {}
TermDocMap = {}

class StopWords(object):
    
    def __init__(self):
        self.stopwords = []
        print("Loading Stopwords from file into memory")
        with open("stopwords.txt") as input_file:
            for input_line_raw in input_file:
                # print type(input_line_raw)
                input_line = unicode(input_line_raw,"utf-8")
                # print type(input_line)
                input_tokens = input_line_raw.split(', ')
                self.stopwords.extend(input_tokens)
    
    def isStopWord(self,token):
    	if token in self.stopwords:
    		return True
    	else: 
    		return False
    
    def printStopWordsToTerminal(self):
        for sw in self.stopwords:
            print(sw)

class TokenStemmer(object):
    
    def getStemmedTokens(self, text):
        content = text.lower()
    	#Tokenizing
    	tokens = []
    	try:
    		tokens = nltk.word_tokenize(text)
    	except Exception as inst:
    		print type(inst)
    		tokens = text.split(" ")
        #Removing StopWords
    	tokens1 = []
    	for token in tokens:
    		if not s_w.isStopWord(token):
    			tokens1.append(token)
    	#Stemming
    	stemTokens = []
    	for token in tokens1:
    		if re.match(primitive_word_detection, token):
    			stemTokens.append(PorterStemmer().stem_word(token))
    		else:
    			stemTokens.append(token)
    	return stemTokens
    

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
        self.infobox_string = ""
        self.infobox_type = ""
        self.categories = []
        self.external_links = []
        
    def processArticle(self):
        print("Processing Article: {0}".format(self.title))
        #print("Text = {0}".format(self.text))
        #First need to extract infobox and remove from Text
        self.getInfoBox()
        #self.getInfoBoxType() #this occurs in getInfoBox...
        self.getCategories()
        self.getExternalLinks()
        #need to remove stopwords from the remaining text
        
    def getInfoBox(self):
        start_match = re.search(infobox_start_detection,self.text)
        #print("start_match = {0}".format(start_match))
        if start_match:
            start_pos = start_match.start()
            #print("start_pos = {0}".format(start_pos))
            if start_pos < 0 :
                return
            brack_count = 2
            end_pos = start_pos + len(INFOBOX_START_STRING)
            while(end_pos < len(self.text)):
                #print("in loop end_pos = {0}".format(end_pos))
                if self.text[end_pos] == '}':
                    brack_count = brack_count - 1
                if self.text[end_pos] == '{':
                    brack_count = brack_count + 1
                if brack_count == 0:
                    break
                end_pos = end_pos+1
            # Malformed infoboxes are not considered.....
            if end_pos+1 >= len(self.text):
                return
            #print("end_pos = {0}".format(end_pos))
            self.infobox_string = self.text[start_pos:end_pos+1]
            #print("infobox_string = {0}".format(self.infobox_string))
            self.text = self.text[0:start_pos] + " " + self.text[end_pos+1:]
            #print("self.text = {0}".format(self.text))
            #self.infobox_string = self.removeCite(self.infobox_string)
            self.infobox_string = self.infobox_string.replace("&gt;",">").replace("&lt;", "<").replace("&amp;", "&").replace("<ref.*?>.*?</ref>", " ").replace("</?.*?>", " ")
            
            new_line_splits = self.infobox_string.split("\n")
            if new_line_splits:
                temp = new_line_splits[0].lower()
                pipe_find = temp.find("|")
                if pipe_find > 0 :
                    temp = temp[0:pipe_find]
                brack_find = temp.find("}}")
                if brack_find > 0 :
                    temp = temp[0:brack_find]
                gt_mark_find = temp.find("<!")
                if gt_mark_find > 0 :
                    temp = temp[0:gt_mark_find]
                temp = temp.replace("{{infobox", "").replace("\n", "").replace("#", "").replace("_"," ").strip()
                self.infobox_type = temp
            for str in new_line_splits:
                if str.find("=") < 0 :
                    continue
                if str.find("{{") >= 0 :
                    bmatches = re.finditer(flower_detection, self.text)
                    if bmatches:
                        for bmatch in bmatches:
                            mtcd = bmatch.group(1)
                            changed = mtcd.replace("|", "-").replace("=", "-")
                            str.replace(mtcd, changed)
                if str.find("|") >= 0 :
                    piped_strings = str.split("|")
                    for ps in piped_strings:
                        key_val = ps.split("=")
                        
                        if len(key_val) != 2 :
                            continue
                        
                        key = key_val[0].replace("|", "").replace("?", "").replace("{", "").replace("}", "").replace("[", "").replace("]", "").strip().lower()   
                        val = key_val[1].replace("[", "").replace("{", "").replace("}", "").replace("[", "").replace("]", "").strip().lower()
                        
                        self.infobox[key] = val
            # print("length of infobox keys = {0}".format(len(self.infobox)))
            # for k in self.infobox:
            #     print "{0} = {1}".format(k,self.infobox[k])
        
    def removeCite(self, string_to_strip):
        start_match = re.search(cite_start_detection,self.text)
        #print("start_match = {0}".format(start_match))
        if start_match:
            start_pos = start_match.start()
            #print("start_pos = {0}".format(start_pos))
            if start_pos < 0 :
                return string_to_strip
            brack_count = 2
            end_pos = start_pos + len(INFOBOX_START_STRING)
            while(end_pos < len(self.text)):
                #print("in loop end_pos = {0}".format(end_pos))
                if self.text[end_pos] == '}':
                    brack_count = brack_count - 1
                if self.text[end_pos] == '{':
                    brack_count = brack_count + 1
                if brack_count == 0:
                    break
                end_pos = end_pos+1
            string_to_strip = string_to_strip[0:start_pos-1] + string_to_strip[end_pos:]
            return removeCite(string_to_strip)
        return string_to_strip
    
    def getInfoBoxType(self):
        if self.infobox_string:
            new_line_splits = self.infobox_string.split("\n")
            if new_line_splits:
                temp = new_line_splits[0].lower()
                pipe_find = temp.find("|")
                if pipe_find > 0 :
                    temp = temp[0:pipe_find]
                brack_find = temp.find("}}")
                if brack_find > 0 :
                    temp = temp[0:brack_find]
                gt_mark_find = temp.find("<!")
                if gt_mark_find > 0 :
                    temp = temp[0:gt_mark_find]
                temp = temp.replace("{{infobox", "").replace("\n", "").replace("#", "").replace("_"," ").strip()
                self.infobox_type = temp
        #print("infobox_type = {0}".format(self.infobox_type))
    
    def getCategories(self):
        matches = re.finditer(category_detection, self.text)
        if matches:
            for match in matches:
                temp = match.group(1).split("|")
                if temp:
                    self.categories.extend(temp)
        #for cat in self.categories:
            #print(cat)
            
    
    def getExternalLinks(self):
        matches = re.finditer(external_links_detection, self.text)
        for match in matches:
            temp = match.group()
            if temp:
                self.external_links.append(temp)
        #for link in self.external_links:
            #print(link)
            
    
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
            self.current_article.processArticle()    #### This is were the processing for the article starts........starts
            indexer = Indexer(self.current_article)
            
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
        # print(type(content))
        # unicode_content = content.encode("utf-8").strip()
        # print(type(unicode_content))
        if content and self.current_element:
            #print("Characters = {0}".format(unicode_content))
            self.current_characters += content + " "
        

class Indexer(object):
    
    def __init__(self, wikiArticle):
        self.wA = wikiArticle
        self.tS = TokenStemmer()
        self.buildTermFreqMap()

    def buildTermFreqMap(self):
        title_tokens = self.tS.getStemmedTokens(self.wA.title)
        for token in title_tokens:
            self.putTokenInTermFreqMap(token)
        link_tokens = self.wA.external_links
        for token in link_tokens:
            self.putTokenInTermFreqMap(token)
        cat_tokens = self.wA.categories
        for token in cat_tokens:
            self.putTokenInTermFreqMap(token)
        for key in self.wA.infobox:
            self.putTokenInTermFreqMap(self.wA.infobox[key])
        text_tokens = self.tS.getStemmedTokens(self.wA.text)
        for token in text_tokens:
            self.putTokenInTermFreqMap(token)
    
    def putTokenInTermFreqMap(self,token):
    	if token not in TermFreqMap:
    		TermFreqMap[token] = 1
    	else:
    		TermFreqMap[token] = TermFreqMap[token] + 1
    	
    	if token not in TermDocMap:
            newlist = []
            newlist.append(1)
            newlist.append(TermFreqMap[token])
            newlist.append(self.wA.id)
            TermDocMap[token] = newlist
    	else:
            oldlist = TermDocMap[token]
            oldlist.insert(0, oldlist[0]+1)
            oldlist.append(TermFreqMap[token])
            oldlist.append(self.wA.id)
            TermDocMap[token] = oldlist
            
class IndexWriter(object):
    def __init__(self):
        fileobj = open(outfile, "ab")
        for key in TermDocMap.keys():
    	    #bytes = bytearray(TermDocMap[key].getByte_List())
    		fileobj.write(bytes(key.encode('utf-8')))
    		#print(key.encode('utf-8'))
    		fileobj.write(bytes(TermDocMap[key]))
    		#print("   "+bytes(TermDocMap[key]))

s_w = StopWords()
#sax.parse("sampleXML.xml", WikiContentHandler())
sax.parse(infile, WikiContentHandler())
IndexWriter() #This writes to outfile....

