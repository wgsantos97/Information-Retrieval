# IMPORTS
import nltk
from nltk.corpus import reuters

# CLASSES
class Doc:
    def __init__(self, n, t):
        self.name = n
        self.rawtext = t

class DocManager:
    def __init__(self, c=""):
        self.category = c
        self.ids = self.getDocs(self.category)
        self.docs = list()
        self.library = dict()
        for id in self.ids:
            text = reuters.raw(id)
            self.docs.append(Doc(id,text))
            self.library[id] = text
    
    def getDocs(self, category):
        allCats = reuters.categories()
        if category in allCats:
            return reuters.fileids(category)
        else:
            print("Error: Invalid Category --> " + category)
            return list()
    
    def getDoc(self, name):
        return self.library[name]

# FUNCTIONS
def main():
    category = "acq"
    d = DocManager(category)
    name = "test/14843"
    print(d.getDoc(name))
    print(name)

main()
