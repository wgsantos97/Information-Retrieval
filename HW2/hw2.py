# HW2
# Author: William Santos
# Date: 9/22/2019
# Description: This program takes sample text from reuters, using the topic "acq".
# With this data set, the code analyzes the text for similarities using two methods.
# One is the Jaccard Similarity and the other is the Cosine Similarity
# This code will generate folders to store the generated data.

# IMPORTS
import os
import nltk
from nltk import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.corpus import reuters
from datetime import datetime
from math import log

# CLASS
class Doc:
    def __init__(self, n, t):
        self.rawtext = t.split()
        t = processText(t)
        self.name = n
        self.text = t
        self.tfrq = termFrequency(t)

    def addToGlobalDict(self):
        for i in self.tfrq:
            key = i[0]
            if key in globalFreq:
                globalFreq[key] += 1
            else:
                globalFreq[key] = 1

    def addToInvertedIdx(self):
        for i in self.tfrq:
            key = i[0]
            if key in invertedIndex:
                invertedIndex[key].append((self.name, self.tfrq[i]))
            else:
                invertedIndex[key] = list()
                invertedIndex[key].append((self.name, self.tfrq[i]))

# FUNCTIONS
def getDocs(category):
    allCats = reuters.categories()
    if category in allCats:
        return reuters.fileids(category)
    else: 
        print("Error: Invalid Category")
        return list()

# Output a list of cleaned tokens
def processText(text):
    all_tokens = word_tokenize(text)
    all_pos_tags = pos_tag(all_tokens)

    no_punct_pos = [(t,pos) for (t,pos) in all_pos_tags if len(pos) > 1] # remove POS tags with length = 1
    lower_tokens = [(t.lower(),pos) for (t,pos) in no_punct_pos] # convert to lower case
    stoplist = stopwords.words('english')
    stoplist.extend(["n't", "'s", ">", "<", "''", "``"])
    good_tokens = [(t,pos) for (t,pos) in lower_tokens if t not in stoplist]
    return good_tokens

def termFrequency(tokens):
    res = dict()
    for i in tokens:
        if i in res:
            res[i] += 1
        else:
            res[i] = 1
    return res

def gatherData(data):
    docs = []
    for doc in data:
        text = reuters.raw(doc)
        docs.append(Doc(doc, text))
    for doc in docs:
        doc.addToGlobalDict()
        doc.addToInvertedIdx()
    return docs

def getSpacing(x):
    line = ""
    space = [4, 8, 12, 16]
    for i in space:
        if(len(x)<i):
            line+="\t"
    return line

def write2a_Results(f, fdict):
    for x in fdict:
        line = "\n" + x + "\t" + getSpacing(x) + ": " + str(fdict[x])
        f.write(line)

def main2a():
    folder = "2a Data"
    if not os.path.exists(folder):
        os.makedirs(folder)
    files = [ folder + "/globalFreq.txt", folder + "/invertedIdx.txt" ]
    fdict = [ globalFreq, invertedIndex ]
    title = [ "Global Frequency", "Inverted Index" ]
    category = "acq"
    docs = getDocs(category)
    data = docs[0:150] # get the first 150
    docs = gatherData(data) # 2a --> build inverted index and a list of document frequencies for all terms and documents
    
    i=0
    for filename in files:
        f = open(filename, "w")
        f.write("Assignment 2a: Inverted Index \nAuthor: William Santos \nDate " + datetime.today().strftime('%m-%d-%Y') + "\nCategory: " + category + "\n\n" + title[i] + ":")
        write2a_Results(f, fdict[i])
        f.close()
        i+=1
    
    return docs

def getIDFSimilarity(query):
    res = dict()
    for t in query:
        key = t[0]
        if key in globalFreq: # if it exists in the inverted index
            for doc in invertedIndex[key]:
                tf = doc[1]
                tf_doc = log(1 + tf)
                idf = log((query[t] + 1) / globalFreq[key]) * -1
                similarity_q_d = query[t] * tf_doc * idf
                if doc[0] in res:
                    res[doc[0]] += similarity_q_d
                else:
                    res[doc[0]] = similarity_q_d
    return res

def getJaccardSimilarity(query):
    res = dict()
    s1 = set(query.split())
    for doc in docs:
        s2 = set(doc.rawtext)
        jc = len(s1.intersection(s2)) / len(s1.union(s2))
        if(jc>0):
            res[doc.name] = jc
    return res

def write2b_Results(f, r, q):
    precisions = [] # 2c calculate precisions
    for ranking in r:
        total = 0
        for i in ranking:
            total += 1
        precisions.append(total/5)

    idx1 = 0
    for ranking in r:
        idx2 = 0
        f.write("\n\nQuery: \"" + q[idx1] + "\"")
        f.write("\nPrecision: " + str(precisions[idx1]))
        f.write("\nFilename\t\t| Similarity Rating")
        f.write("\n======================================")
        for i in ranking:
            line = "\n" + str(idx2+1) + ") " + i[0] + "\t| " + str(i[1])
            f.write(line)
            idx2 += 1
        idx1 += 1

def main2b():
    folder = "2b Data"
    if not os.path.exists(folder):
        os.makedirs(folder)
    files = [ "TF_IDF Similarity Results.txt", "Jaccard Similarity Results.txt" ]
    method = [ "TF_IDF Similarity", "Jaccard Similarity" ]
    
    queries = [ "banking", "financial bank pay", "financial analyst profitable" ]

    q = queries.copy()
    results1 = []
    results2 = []

    # Get Jaccard
    for query in queries:
        temp = getJaccardSimilarity(query)
        res = sorted(temp.items(), key = lambda x: x[1], reverse=True)
        results2.append(res)

    # Get Cosine
    for i in range(0,len(queries)):
        queries[i] = processText(queries[i])
        tf_query = termFrequency(queries[i])
        temp = getIDFSimilarity(tf_query)
        res = sorted(temp.items(), key = lambda x: x[1], reverse=True)      
        results1.append(res)
    
    results = [ results1, results2 ]

    idx=0
    for filename in files:
        f = open(folder + "/" + filename, "w")
        f.write("Assignment 2b: Similarity Comparison \nAuthor: William Santos \nDate " + datetime.today().strftime('%m-%d-%Y') + "\nMethod: " + method[idx] + "\n\nQuery Results:")
        write2b_Results(f, results[idx], q)
        f.close()
        idx+=1

def getStatistics():
    filename = "statistics.txt"
    max = 0
    maxName = ""
    min = 1000000000
    minName = ""
    total = 0
    count = 0
    avg = 0
    for doc in docs:
        x = len(doc.rawtext)
        if(x>max):
            max = x
            maxName = doc.name
        if(x<min):
            min = x
            minName = doc.name
        total+=x
        count+=1
    avg = total/count

    f = open(filename, "w")
    f.write("Assignment 2c: Statistics Report \nAuthor: William Santos \nDate " + datetime.today().strftime('%m-%d-%Y') + "\n\nReport:")
    f.write("\nBefore NLP")
    f.write("\n=================================================================")
    f.write("\nNumber of Documents:\t" + str(count))
    f.write("\nAverage Document Length:\t" + str(avg) + " words")
    f.write("\nMax Document Length -->\t" + maxName + "\t: " + str(max) + " words")
    f.write("\nMin Document Length -->\t" + minName + "\t: " + str(min) + " words")

    max = 0
    min = 1000000000
    total = 0
    count = 0
    for doc in docs:
        x = len(doc.text)
        if(x>max):
            max = x
            maxName = doc.name
        if(x<min):
            min = x
            minName = doc.name
        total+=x
        count+=1
    avg = total/count

    f.write("\n\nAfter NLP")
    f.write("\n=================================================================")
    f.write("\nNumber of Documents:\t" + str(count))
    f.write("\nAverage Document Length:\t" + str(avg) + " words")
    f.write("\nMax Document Length -->\t" + maxName + "\t: " + str(max) + " words")
    f.write("\nMin Document Length -->\t" + minName + "\t: " + str(min) + " words")
    f.close()

# MAIN
globalFreq = dict()
invertedIndex = dict()
docs = main2a()
main2b()
getStatistics()