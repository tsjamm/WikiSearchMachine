# WikiSearchMachine
A Wikipedia Dump Search Engine in Python

Writen for the Information Retrieval and Extraction Course Spring 2015 at IIIT-H


The Wiki Parser uses python's SAX parser to parse the tags of the Wiki Markup

Parser.py is to be executed for parsing and indexing.

The Tokenizer and Stemmer (PorterStemmer) are from ntlk, it must be installed

The title, text, infobox, categories, are case-folded, tokenized and indexed.

The search query can be regular words, or can be fielded query like t:lord b:rings

Searcher.py is the main file to be executed for searching



(c) 2015 Sai Teja Jammalamadaka