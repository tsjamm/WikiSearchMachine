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
import os.path

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

freq_string_detection = re.compile("([0-9]*)t([0-9]*)b([0-9]*)c([0-9]*)i([0-9]*)")

TermFreqMap = {}
#TermDocMap = {}

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
        self.infobox_values_string = ""
        self.infobox_type = ""
        self.categories = []
        self.external_links = []
        
    def processArticle(self):
        #print("Processing Article: {0}".format(self.title.encode('utf-8')))
        #print("Text = {0}".format(self.text))
        #First need to extract infobox and remove from Text
        self.getInfoBox()
        self.getInfoBoxValuesString()
        #self.getInfoBoxType() #this occurs in getInfoBox...
        self.getCategories()
        self.getExternalLinks()
        self.makeTextAlphaNumeric()
        
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
    
    def getInfoBoxValuesString(self):
        ib_val_string = ""
        for key in self.infobox:
            ib_val_string += re.sub(u'[^a-zA-Z]+',' ',self.infobox[key])
            ib_val_string += " "
        self.infobox_values_string = ib_val_string
    
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
        re.sub(category_detection, ' ', self.text) # this is for removing the category headings....
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
    
    def makeTextAlphaNumeric(self):
        self.text = re.sub(u'[^a-zA-Z]+', ' ', self.text)
        self.title = re.sub(u'[^a-zA-Z]+', ' ', self.title)
        for key in self.infobox:
            self.infobox[key] = re.sub(u'[^a-zA-Z]+',' ',self.infobox[key])
        newCats = []
        for cat in self.categories:
            cat = re.sub(u'[^a-zA-Z]+',' ',cat)
            newCats.append(cat)
        self.categories = newCats
        
    
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
        self.checkTermFreqMapSizeAndWrite()

    def buildTermFreqMap(self):
        title_tokens = self.tS.getStemmedTokens(self.wA.title)
        for token in title_tokens:
            self.putTitleTokenInTermFreqMap(token)
        #link_tokens = self.wA.external_links
        #for token in link_tokens:
        #    self.putTokenInTermFreqMap(token)
        cat_tokens = self.tS.getStemmedTokens(self.getStringFromListofStrings(self.wA.categories))
        for token in cat_tokens:
            self.putCatTokenInTermFreqMap(token)
        ib_tokens = self.tS.getStemmedTokens(self.wA.infobox_values_string)
        for token in ib_tokens:
            self.putIBTokenInTermFreqMap(token)
        # for key in self.wA.infobox:
        #     if self.wA.infobox[key] != '':
        #         self.putIBTokenInTermFreqMap(self.wA.infobox[key])
        text_tokens = self.tS.getStemmedTokens(self.wA.text)
        for token in text_tokens:
            self.putBodyTokenInTermFreqMap(token)
    
    def checkTermFreqMapSizeAndWrite(self):
        if len(TermFreqMap) > 2000:
            IndexWriter().mergeWriter()
            
    
    def checkIfTokenInTermFreqMap(self,token):
        
        if token not in TermFreqMap:
            freq_obj = {}
            TermFreqMap[token] = freq_obj
        if self.wA.id not in TermFreqMap[token]:
            freq_doc_obj = {}
            freq_doc_obj["t"] = 0 #title
            freq_doc_obj["b"] = 0 #body
            freq_doc_obj["c"] = 0 #cat
            freq_doc_obj["i"] = 0 #infobox
            TermFreqMap[token][self.wA.id] = freq_doc_obj
    
    def putTitleTokenInTermFreqMap(self,token):
        self.checkIfTokenInTermFreqMap(token)
        TermFreqMap[token][self.wA.id]["t"] += 1
        
    def putBodyTokenInTermFreqMap(self,token):
        self.checkIfTokenInTermFreqMap(token)
        TermFreqMap[token][self.wA.id]["b"] += 1
        
    def putCatTokenInTermFreqMap(self,token):
        self.checkIfTokenInTermFreqMap(token)
        TermFreqMap[token][self.wA.id]["c"] += 1
        
    def putIBTokenInTermFreqMap(self,token):
        self.checkIfTokenInTermFreqMap(token)
        TermFreqMap[token][self.wA.id]["i"] += 1
    
    def getStringFromListofStrings(self,list):
        toReturn = ""
        for str in list:
            toReturn += str + " "
        return toReturn
            
class IndexWriter(object):
    def __init__(self):
        if not os.path.exists(outfile):
            out_file = open(outfile,"w")
            out_file.close()
        if not os.path.exists(outfile+".tmp"):
            temp_file = open(outfile+".tmp","w")
            temp_file.close()
    #     fileobj = open(outfile, "a")
    #     for word in TermFreqMap:
    #         toWrite = u"" + word + "="
    #         fo = TermFreqMap[word]
    #         for did in fo:
    #             toWrite += did+":"
    #             fdo = fo[did]
    #             tfreq = fdo["t"]
    #             bfreq = fdo["b"]
    #             cfreq = fdo["c"]
    #             ifreq = fdo["i"]
    #             total_freq = tfreq+bfreq+cfreq+ifreq
    #             toWrite += "{0}t{1}b{2}c{3}i{4};".format(total_freq,tfreq,bfreq,cfreq,ifreq)
    #         toWrite += "\n"
    #         fileobj.write(toWrite.encode('utf-8'))
    
    def getFOFromLine(self,fline):
        freq_obj = {}
        docs = fline.split(';')
        for doc in docs:
            parts = doc.split(':')
            did = parts[0]
            freq_doc_obj = {}
            fstring = parts[1]
            matches = re.finditer(freq_string_detection, fstring)
            if matches:
                for match in matches:
                    total = int(match.group(1))
                    title = int(match.group(2))
                    body = int(match.group(3))
                    cat = int(match.group(4))
                    infob = int(match.group(5))
                    freq_doc_obj["t"] = title #title
                    freq_doc_obj["b"] = body #body
                    freq_doc_obj["c"] = cat #cat
                    freq_doc_obj["i"] = infob #infobox
            freq_obj[did] = freq_doc_obj
        return freq_obj
    
    def getNewFO(self, word, ffo):
        mfo = TermFreqMap[word]
        cfo = dict(mfo.items() + ffo.items())
        return cfo
    
    def removeMFO(self,word):
        del TermFreqMap[word]
    
    def mergeWriter(self):
        with open(outfile+".tmp","w") as temp_file:
            with open(outfile,"r") as old_file:
                for line in old_file:
                    parts = line.split('=')
                    if len(parts) == 2:
                        word = parts[0]
                        ffo = self.getFOFromLine(parts[1])
                        cfo = self.getNewFO(word, ffo)
                        self.removeMFO(word)
                        toWrite = u"" + word + "="
                        for did in cfo:
                            toWrite += did+":"
                            fdo = fo[did]
                            tfreq = fdo["t"]
                            bfreq = fdo["b"]
                            cfreq = fdo["c"]
                            ifreq = fdo["i"]
                            total_freq = tfreq+bfreq+cfreq+ifreq
                            toWrite += "{0}t{1}b{2}c{3}i{4};".format(total_freq,tfreq,bfreq,cfreq,ifreq)
                        toWrite += "\n"
                        temp_file.write(toWrite.encode('utf-8'))
            for word in TermFreqMap:
                toWrite = u"" + word + "="
                fo = TermFreqMap[word]
                for did in fo:
                    toWrite += did+":"
                    fdo = fo[did]
                    tfreq = fdo["t"]
                    bfreq = fdo["b"]
                    cfreq = fdo["c"]
                    ifreq = fdo["i"]
                    total_freq = tfreq+bfreq+cfreq+ifreq
                    toWrite += "{0}t{1}b{2}c{3}i{4};".format(total_freq,tfreq,bfreq,cfreq,ifreq)
                toWrite += "\n"
                temp_file.write(toWrite.encode('utf-8'))
            
        
        with open(outfile+".tmp","r") as temp_file:
            with open(outfile,"w") as new_file:
                for line in temp_file:
                    new_file.write(line)
        
        with open(outfile+".tmp","w") as temp_file:
            print("tempfile copied and erased")


s_w = StopWords()
#sax.parse("sampleXML.xml", WikiContentHandler())
sax.parse(infile, WikiContentHandler())
IndexWriter().mergeWriter() #This writes to outfile....

