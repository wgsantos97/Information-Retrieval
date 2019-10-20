from bs4 import BeautifulSoup
import requests

#CLASSES
class LinkObject:
    def __init__(self, link):
        self.link = link
        self.raw = self.getSoup()
        self.title = self.getTitle()
        self.text = self.getText()
    
    def getSoup(self):
        r = requests.get(self.link)
        return BeautifulSoup(r.text, features="html.parser")
    
    def getTitle(self):
        return self.raw.find("h1").text

    def getText(self):
        pData = self.raw.find_all("p")
        text = list()
        for p in pData:
            text.append(p.get_text())
        return text

class LinkObjectCore(LinkObject):
    def __init__(self, link, linkFilter):
        super().__init__(link)
        self.linkFilter = linkFilter
        self.LinkObjectLibrary = dict()
        self.LinkObjectLibrary[self.title] = self.text
        self.LinkList = self.getLinks()

    def getLinks(self):
        res = list()
        links_data = self.raw.find_all('a')  # finds all tags with 'a'
        for link in links_data:
            href = link.get('href')
            if(href is None or len(href)<5 or href[0] == '#'):
                continue
            if(href[0] == '/'):
                href = self.linkFilter + href
            if(self.linkFilter not in href):
                continue
            res.append(href)
        return res

    def processLinkNeighbors(self):
        for link in self.LinkList:
            obj = LinkObject(link)
            self.LinkObjectLibrary[obj.title] = obj.text
        return self.LinkObjectLibrary

# MAIN
def main():
    link = "https://avatar.fandom.com/wiki/Zaheer"
    linkFilter = "https://avatar.fandom.com"
    mainLink = LinkObjectCore(link, linkFilter)
    result = mainLink.processLinkNeighbors()
    print(result.keys())

main()
