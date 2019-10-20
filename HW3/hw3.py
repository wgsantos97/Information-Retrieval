# HW 3
# Author: William Santos
# Date: 9/29/2019
# Description: 
# 

# IMPORTS
import os
import nltk
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.corpus import reuters
from datetime import datetime
from math import log

# CLASSES
class Doc:
    def __init__(self, n, t, nlp):
        self.rawtext = t
        t = nlp.processText(t)
        self.name = n
        self.text = t
        self.tfrq = self.termFrequency(t)
        self.length = sum(self.tfrq.values())

    def termFrequency(self, t):
        res = dict()
        for i in t:
            if i in res:
                res[i] += 1
            else:
                res[i] = 1
        return res

    def addToGlobalDict(self, d):
        for i in self.tfrq:
            if i in d:
                d[i] += 1
            else:
                d[i] = 1
        return d

    def addToInvertedIndex(self,d):
        for i in self.tfrq:
            if i in d:
                d[i].append((self.name, self.tfrq[i]))
            else:
                d[i] = list()
                d[i].append((self.name, self.tfrq[i]))
        return d

class NLP_Data:
    def __init__(self, c = "", f = ""):
        self.globalFreq = dict()
        self.invertedIdx = dict()
        self.library = dict()
        self.category = c
        self.folder = f
        self.docs = self.startNLP()
        self.corpusLength = self.getCorpusLength()

    def getCorpusLength(self):
        res = 0
        for doc in self.docs:
            res += doc.length
        return res

    def startNLP(self):
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
        files = [ "globalFreq.txt", "invertedIdx.txt" ]
        titles = [ "Global Frequency", "Inverted Index" ]
        filepaths = [ (self.folder + "/" + x) for x in files ]
        fdict = [ self.globalFreq, self.invertedIdx ]
        docs = self.gatherData(self.getDocs(self.category)[:150])
        
        i=0
        for path in filepaths:
            f = open(path,"w")
            f.write("Assignment 3: " + titles[i] + "\nAuthor: William Santos \nDate " + datetime.today().strftime('%m-%d-%Y') + "\nCategory: " + self.category + "\n\n" + titles[i] + ":" )
            self.write3a_Results(f,fdict[i])
            f.close()
            i+=1
        return docs

    def write3a_Results(self, f,fdict):
        for x in fdict:
            line = "\n" + x + "\t" + self.getSpacing(x) + ": " + str(fdict[x])
            f.write(line)

    def getSpacing(self, x):
        tabs = ""
        space = [4,8,12,16,20]
        for i in space:
            if(len(x)<i):
                tabs+="\t"
        return tabs

    def gatherData(self, data):
        docs = []
        for doc in data:
            text = reuters.raw(doc)
            docs.append(Doc(doc,text,self))
        for doc in docs:
            self.library[doc.name] = doc.rawtext
            self.globalFreq.update(doc.addToGlobalDict(self.globalFreq))
            self.invertedIdx.update(doc.addToInvertedIndex(self.invertedIdx))
        return docs
        

    def getDocs(self, category):
        allCats = reuters.categories()
        if category in allCats:
            return reuters.fileids(category)
        else:
            print("Error: Invalid Category --> " + category)
            return list()

    def fixTag(self, nltk_tag):
        if nltk_tag.startswith('J'):
            return wordnet.ADJ
        elif nltk_tag.startswith('V'):
            return wordnet.VERB
        elif nltk_tag.startswith('N'):
            return wordnet.NOUN
        elif nltk_tag.startswith('R'):
            return wordnet.ADV
        else:
            return None

    # Output a list of cleaned tokens
    def processText(self, text):
        all_tokens = word_tokenize(text) # convert to tokens
        all_pos_tags = pos_tag(all_tokens) # tag tokens

        # Convert to Lower Case
        lower_tokens = [ t.lower() for (t,pos) in all_pos_tags ]

        # Remove Stopwords
        stoplist = stopwords.words('english')
        stoplist.extend([ ">", "<", ")", "(", "``", "''", ".", "'", ";", "'s", ",", "n't" ])
        stoplist_tokens = [ t for t in lower_tokens if t not in stoplist]
        stoplist_tokens = " ".join(stoplist_tokens)

        # Stem the words
        lemmatizer = WordNetLemmatizer()
        nltk_tagged = nltk.pos_tag(nltk.word_tokenize(stoplist_tokens))
        wn_tagged = map(lambda x: (x[0], self.fixTag(x[1])), nltk_tagged)
        result = []
        for word, tag in wn_tagged:
            if tag is None:
                result.append(word)
            else:
                result.append(lemmatizer.lemmatize(word,tag))

        return result

class scoringMethod():
    def __init__(self, nlp, n="", f=""):
        self.nlp = nlp
        self.docs = nlp.docs
        self.name = n
        self.folder = f
        self.results = dict()
        self.ranking = list()
    
    def query(self, q, l):
        for doc in self.docs:
            self.results[doc.name] = self.eval(doc, q, l)
        self.ranking = sorted(self.results.items(), key = lambda x: x[1], reverse=True)
        return self.ranking

    # d - document; q - query; v - value
    def eval(self, d, q, v):
        print("Error: Must implement evaluation system that updates the results dictionary.")
        return -1
    
    def writeResults(self, filename, query, smoothing, results):
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
        path = self.folder + "/" + filename

        f = open(path, "w")
        f.write("Assignment 3b: Statistics Report \nAuthor: William Santos \nDate: " + datetime.today().strftime('%m-%d-%Y'))
        f.write("\nMethod: " + self.name + "\n\nQuery: " + query)
        i=0
        for x in smoothing:
            f.write("\n\nSmoothing: " + str(x))
            for y in results[i][:5]:
                f.write("\n" + y[0] + " :\t" + str(y[1]))
            i+=1
        f.close()

class jelinerMercer(scoringMethod):
    # Override default eval
    def eval(self, d, q, l): # lambda smoothing
        query = q.split()
        res = 0
        for word in query:
            a=0
            if word in d.tfrq:
                a = d.tfrq[word]/d.length
            b=0
            if word in self.nlp.invertedIdx:
                total = 0
                for x in self.nlp.invertedIdx[word]:
                    total+=x[1]
                b = (total/self.nlp.corpusLength)
            res += (1-l) * a + l * b
        return res

class dirichletPrior(scoringMethod):
    def eval(self, d, q, m): # mu smoothing
        query = q.split()
        res = 0
        for word in query:
            a = (d.length/(d.length + m))
            b = 0
            if word in d.tfrq:
                b = d.tfrq[word]/d.length
            c = (m/(d.length+m))
            d1 = 0
            if word in self.nlp.invertedIdx:
                total = 0
                for x in self.nlp.invertedIdx[word]:
                    total+=x[1]
                d1 = (total/self.nlp.corpusLength)
            res += a*b + c*d1
        return res

def main():
    nlp = NLP_Data("acq","3a Data")
    queries = [
        "financial banking pay", 
        "financial banking analyst profitable",
        "financial analyst profitable job high pay",
    ]

    n = 1
    for q in queries:
        n1 = "Jelinek Mercer"
        lam = [ 0.3, 0.6, 0.9 ]
        i=0
        j = jelinerMercer(nlp, n1, "3b Data")
        r1 = list()
        while(i<3):
            r1.append(j.query(q, lam[i]))
            i+=1
        j.writeResults(n1 + "_Q" + str(n) + ".txt", q, lam, r1)

        n2 = "Dirichlet Prior"
        mu = [ 1, 50, 100 ]
        i=0
        d = dirichletPrior(nlp, n2, "3b Data")
        r2 = list()
        while(i<3):
            r2.append(d.query(q,mu[i]))
            i+=1
        d.writeResults(n2 + "_Q" + str(n) + ".txt", q, mu, r2)
        n+=1
    

# MAIN
main()