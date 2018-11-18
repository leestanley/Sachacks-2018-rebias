# import libraries
import urllib.request
from bs4 import BeautifulSoup
from w3lib.html import replace_entities

def nyt(soup):
    soup 
    soup_list = soup.select('article p')
    replace_entities('&#8217;')
    soup_str = ''
    for x in soup_list:
        soup_str += x.text + ' '
    final = ''
    for x in range(len(soup_str)):
        if ord(soup_str[x]) == 8217:
            if soup_str[x-1] != ' ' and soup_str[x+1] != ' ':
                final += "'"
        else:
            final += soup_str[x]
    return final

def guardian(soup):
    pass

def bbc(soup):
    pass

def econ(soup):
    pass

def usa(soup):
    pass

def fortune(soup):
    pass

def hill(soup):
    pass

def wsj(soup):
    pass

def cnn(soup):
    return soup.find("article").find("h1").string

def ap(soup):
    pass

def getSoup(url):
    srcs = ['nytimes', 'guardian', 'bbc', 'economist', 'usatoday', 'fortune', 'thehill', 'wsj', 'cnn', 'ap']
    src_content = {'nytimes': nyt, 'guardian': guardian, 'bbc': bbc, 'economist': econ, 'usatoday': usa, 'fortune': fortune, 'thehill': hill, 'wsj': wsj, 'cnn': cnn, 'ap': ap}
    req = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"}) 
    page = urllib.request.urlopen(req)
    soup = BeautifulSoup(page, 'html.parser')
    source = ''
    for x in srcs:
        if x in url:
            source = x
            break
    content = src_content[source](soup)
    return content


def main():
    url = 'https://www.nytimes.com/2018/11/16/us/voting-machines-florida.html?action=click&module=Top%20Stories&pgtype=Homepage'
    print(getSoup(url))

if __name__ == '__main__':
    main()
