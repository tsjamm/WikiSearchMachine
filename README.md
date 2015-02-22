# WikiSearchMachine
A Wikipedia Dump Search Engine in Python
---

Writen for the Information Retrieval and Extraction Course Spring 2015 at IIIT-H

### Summary
The Wiki Parser uses python's SAX parser to parse the tags of the Wiki Markup. Parser.py is to be executed for parsing and indexing. The Tokenizer and Stemmer (PorterStemmer) are from ntlk, it must be installed. The title, text, infobox, categories, are case-folded, tokenized, stemmed and indexed. The search query can be regular words, or can be fielded query like t:lord b:rings . Searcher.py is the main file to be executed for searching
run_index.sh and run.sh contain the Parser.py and Searcher.py execution commands respectively



### The Given Problem

The given problem was to design and develop a scalable and efficient search engine using the Wikipedia data.
Requirements:
* ~50 GB of Wikipedia data (Downloaded compressed file is ~11GB)
* Results obtained in less than a sec (even for long queries) 
* Supports field queries (ex: title) 
* Index size should be less than 1/4 of the data size. 
* You have to build your own indexing mechanism, i.e. you cannot use Nutch or Lucene to index the Wikipedia data.
Platform:
* OS: Preferably Linux
* Languages: Java/C++/Python


### My Approach

There are a number of ways to parse an XML file. The worst way, but brute force way is to maintain the entire XML structure in memory by loading the entire file into memory. This would work for small files, but for huge files, it would not scale.

The optimal way to do it is by using the SAX parser (Simple API for XML)
The SAX parser traverses the file line by line and triggers specific functions whenever there is an opening tag, content, and closing tag. This allows us to parse through the file without having to load the entire structure into memory.

Thus we can decide how many articles to process during the parsing itself.

Using this approach, we extract each Wikipedia article as an object, and then pass it to an Indexer Module. This module analyses the article, takes the necessary text components, tokenizes them, and creates a frequency map of the word and documents it occurs in. The tokenization uses case folding and stemming (Porter Stemmer in Python) so as to cover various word cases.

Now this map can not be stored in memory at once, so dump the map to temporary files for every 10,000 Wikipedia articles, and then merge them together at the end. Then we sort the final file and output compressed part files for us to access in an easy way, and reduce the index size.

The searching takes a query and breaks it down the same way (tokenization, case folding, stemming) and tries to extract the frequency from the index. Then we calculate the TFIDF (Term Frequency - Inverse Document Frequency) for each word and document and generate a ranked list of Wikipedia article titles as the end result.

### My Implementation

I wrote the following python program that can parse a Wikipedia dump XML file and index it in index files. These can then be used to search for articles through a simple searching algorithm.

This implementation is very slow and not optimized, it is far from the ideal, but it gets the job done.

Once you clone the project (or download the zip and uncompress it) you will see ans src folder, and some other files.

The src folder contains the python code split into various .py files for ease of maintenance

In the main folder you will find some .sh (for Linux) files or .bat (for Windows) files.

Though the code works on Windows, I would not advice running it in windows as there are memory constraints that windows might fail to satisfy (a 64-bit windows gives at max 2GB of RAM to a 32-bit process such as our python script, and the indexer might fail to index; Linux does a better job of giving about 3GB ). Of course this memory constraint is if you run it on the ~50 GB Wikipedia dump file, not the sample 100 article subset that I provided.

In order to run the indexer, create a folder named Index the main directory (alongside src)
I provided a sample file with 100 Wikipedia articles that illustrates the concept of indexing and searching.

On Linux open the terminal and run:
```bash
$ sh run_indexer.sh ./sampleXML.xml ./Index/index
```

On Windows open the command prompt and run:
```bash
> run_indexer.bat sampleXML.xml Index\index
```

The indexer should start running, it might take a while, and you will get a completion message with time statistics displayed in counts of milliseconds taken.


For testing the searching, you can try 2 types of queries:
* Regular Queries - just plain text
* Fielded Queries - words with specific criteria, like t:lord b:rings, where t: means search in title, b: means search in body. You can use 4 types, namely t: for title, b: for body, c: for category, i: for infobox

For testing the query create a text file in the main directory with the first line as the number of queries, and subsequent lines will contain one query per line. An example is given in testQuery.txt

On Linux open the terminal and run:
```bash
$ sh run.sh ./Index/index < testQuery.txt
```

On Windows, open the command prompt and run:
```bash
> run.bat Index\index < testQuery.txt
```

You should see the top 10 results available (maximum) per each query




(c) 2015 Sai Teja Jammalamadaka
