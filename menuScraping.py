# import libraries
import urllib.request
from bs4 import BeautifulSoup


def nyt(soup):
    soup_list = soup.select('.css-1ebnwsw')
    soup_str = ''
    for x in soup_list:
        soup_str += x.text + ' '
    final = ''
    for x in range(len(soup_str)):
        if ord(soup_str[x]) == 8217:
            if soup_str[x - 1] != ' ' and soup_str[x + 1] != ' ':
                final += "'"
        else:
            final += soup_str[x]
    return final


def guardian(soup):
    soup_list = soup.select('div > div > div > div > p')
    soup_str = ''
    for x in soup_list:
        soup_str += x.text + ' '
    final = ''
    for x in range(len(soup_str)):
        if ord(soup_str[x]) == 8217:
            if soup_str[x - 1] != ' ' and soup_str[x + 1] != ' ':
                final += "'"
        else:
            final += soup_str[x]
    return final


def bbc(soup):
    soup_list = soup.select('div > div > div > div > p')
    soup_str = ''
    for x in soup_list:
        soup_str += x.text + ' '
    final = ''
    for x in range(len(soup_str)):
        if ord(soup_str[x]) == 8217:
            if soup_str[x - 1] != ' ' and soup_str[x + 1] != ' ':
                final += "'"
        else:
            final += soup_str[x]
    return final


def econ(soup):
    soup_list = soup.select('article > div > div > p')
    soup_str = ''
    for x in soup_list:
        soup_str += x.text + ' '
    final = ''
    for x in range(len(soup_str)):
        if ord(soup_str[x]) == 8217:
            if soup_str[x - 1] != ' ' and soup_str[x + 1] != ' ':
                final += "'"
        else:
            final += soup_str[x]
    return final


def usa(soup):
    soup_list = soup.select('article > div > p')
    soup_str = ''
    for x in soup_list:
        soup_str += x.text + ' '
    final = ''
    for x in range(len(soup_str)):
        if ord(soup_str[x]) == 8217:
            if soup_str[x - 1] != ' ' and soup_str[x + 1] != ' ':
                final += "'"
        else:
            final += soup_str[x]
    return final


def fortune(soup):
    soup_list = soup.select('div > div > div > p')
    soup_str = ''
    for x in soup_list:
        soup_str += x.text + ' '
    final = ''
    for x in range(len(soup_str)):
        if ord(soup_str[x]) == 8217:
            if soup_str[x - 1] != ' ' and soup_str[x + 1] != ' ':
                final += "'"
        else:
            final += soup_str[x]
    return final


def hill(soup):
    soup_list = soup.select('article > div > div > div > div > div > p')
    soup_str = ''
    for x in soup_list:
        soup_str += x.text + ' '
    final = ''
    for x in range(len(soup_str)):
        if ord(soup_str[x]) == 8217:
            if soup_str[x - 1] != ' ' and soup_str[x + 1] != ' ':
                final += "'"
        else:
            final += soup_str[x]
    return final


# def wsj(soup):
#     soup_list = soup.select('div > div > div > div > p')
#     soup_str = ''
#     for x in soup_list:
#         soup_str += x.text + ' '
#     final = ''
#     for x in range(len(soup_str)):
#         if ord(soup_str[x]) == 8217:
#             if soup_str[x - 1] != ' ' and soup_str[x + 1] != ' ':
#                 final += "'"
#         else:
#             final += soup_str[x]
#     return final


def cnn(soup):
    soup_list = soup.select('.zn-body__paragraph')
    soup_str = ''
    for x in soup_list:
        soup_str += x.text + ' '
    final = ''
    for x in range(len(soup_str)):
        if ord(soup_str[x]) == 8217:
            if soup_str[x - 1] != ' ' and soup_str[x + 1] != ' ':
                final += "'"
        else:
            final += soup_str[x]
    return final.replace('CNN', 'Source')


def ap(soup):
    soup_list = soup.select('div > div > div > p')
    soup_str = ''
    for x in soup_list:
        soup_str += x.text + ' '
    final = ''
    for x in range(len(soup_str)):
        if ord(soup_str[x]) == 8217:
            if soup_str[x - 1] != ' ' and soup_str[x + 1] != ' ':
                final += "'"
        else:
            final += soup_str[x]
    return final.replace('AP', 'Source')


def getSoup(url):
    srcs = ['nytimes', 'guardian', 'bbc', 'economist', 'usatoday', 'fortune', 'thehill', 'cnn', 'ap']
    src_content = {'nytimes': nyt, 'guardian': guardian, 'bbc': bbc, 'economist': econ, 'usatoday': usa, 'fortune': fortune, 'thehill': hill, 'cnn': cnn, 'ap': ap}
    req = urllib.request.Request(url, headers={'User-Agent': "Magic Browser"})
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
    url = 'https://www.apnews.com/8fd63a7696fe4bb3855bda2d4b3e7943'
    print(getSoup(url))


if __name__ == '__main__':
    main()
