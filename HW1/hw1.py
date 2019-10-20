import nltk
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk import pos_tag
from collections import Counter
from nltk.corpus import stopwords

#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')
#nltk.download('stopwords')

filename = 'alice.txt' # EDIT this as needed to read different text files

def getDict(section):
    d = dict()
    for sent in section:
        for w in sent:
            if w in d:
                d[w] += 1
            else:
                d[w] = 1
    return d

# or read all lines
def read_all_lines():
    f = open(filename, 'r')
    all_lines = ' '.join(f.readlines())  # joins the lines together
    f.close()
    return all_lines

def getResults(message, topList):
    c = 1
    print(message)
    for x in topList:
        print(str(c) + ")", x[0], ":", x[1])
        c+=1


text = read_all_lines() # get entire text
sentences = sent_tokenize(text) # extract sentences
tokens = [] 
tags = []

for i in sentences:
    words = word_tokenize(i) # extract each word
    final = [] # 
    for w in words: # for each word in the list of words taken from a sentence
        w = w.lower()
        if(w.isalnum() and w not in stopwords.words('english')): # filter out all non alphanumeric characters and stopwords
            final.append(w)
    
    tags.append(pos_tag(final)) # generate tag
    tokens.append(final) # add to list of tokens

dict1 = getDict(tokens)
k = Counter(dict1)
k = k.most_common()
top5 = k[:5] # get top 5 items
bottom5 = k[-5:] # get bottom 5 items
bottom5.reverse()

print("RESULTS:")
getResults("Top 5 Most Common Words", top5)
getResults("Top 5 Least Common Words", bottom5)
