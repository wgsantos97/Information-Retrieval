from bs4 import BeautifulSoup
import requests

r = requests.get('https://www.tensorflow.org/get_started/mnist/beginners')
#print(r.text)  # prints the whole web page

soup = BeautifulSoup(r.text)

# extract text only
text_only = soup.get_text()
print(text_only)  

# extract links from the web-page

print('\n +++++++++++++THESE ARE THE LINKS AND THE ANCHORS ON THE WEB PAGE \n')
links_data = soup.find_all('a')  # finds all tags with 'a'
for link in links_data: 
    print(link.get('href'), ' ', link.get_text())  # returns the url addresses found in the web page

title = soup.find('title')  
print(title.get_text())  # prints the content of the title tag

#import urllib.request as url  #didn't work with https url's only with http
# this works because it is http not https
#r = url.urlopen('http://web.stanford.edu/~zlotnick/TextAsData/
#Web_Scraping_with_Beautiful_Soup.html')
