# import libraries
import urllib.request
from bs4 import BeautifulSoup

def nyt(soup):
    return soup.find("article").find("span").string

def lat(soup):
    pass

def bbc(soup):
    pass

def forbes(soup):
    pass

def usa(soup):
    pass

def csm(soup):
    pass

def hill(soup):
    pass

def wsj(soup):
    pass

def cnn(soup):
    return soup.find("article").find("h1").string

def ap(soup):
    pass

def getSoup():
    titles = []
    srcs = ['nytimes', 'latimes', 'bbc', 'forbes', 'usatoday', 'csm', 'thehill', 'wsj', 'cnn', 'ap']
    src_titles = {'nytimes': nyt, 'latimes': lat, 'bbc': bbc, 'forbes': forbes, 'usatoday': usa, 'csm': csm, 'thehill': hill, 'wsj': wsj, 'cnn': cnn, 'ap': ap}
    urls = ["https://www.cnn.com/2018/11/17/us/california-fires-wrap/index.html", "https://www.nytimes.com/2018/11/17/us/usa-voting-system-elections.html?action=click&module=Top%20Stories&pgtype=Homepage", "https://www.nytimes.com/2018/11/16/us/voting-machines-florida.html?action=click&module=Top%20Stories&pgtype=Homepage"]
    for url in urls:
        req = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"}) 
        page = urllib.request.urlopen(req)
        soup = BeautifulSoup(page, 'html.parser')
        source = ''
        for x in srcs:
            if x in url:
                source = x
                break
        title = src_titles[source](soup)
        final = ''
        for x in title[:]:
            if ord(x) > 1000:
                final += chr(39)
            else:
                final += x
        titles.append((final, url))
    for x in titles:
        print(x)

def main():
    getSoup()

if __name__ == '__main__':
    main()
