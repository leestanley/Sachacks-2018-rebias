# import libraries
import urllib.request
from bs4 import BeautifulSoup

def getSoup():
    menu = "https://menus.calpolycorporation.org/805kitchen/"
    req = urllib.request.Request(menu, headers={'User-Agent' : "Magic Browser"}) 
    page = urllib.request.urlopen(req)
    soup = BeautifulSoup(page, 'html.parser')
    # return soup
    print(soup)

def main():
    getSoup()
    # a = getSoup()
#     return a


if __name__ == '__main__':
    main()
