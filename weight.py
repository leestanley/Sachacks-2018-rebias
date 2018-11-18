# import main
import numpy as np
from datascience import Table
bias = Table().read_table("bias.csv").select("News Source", "Horizontal Rank")
news_sources = bias.column("News Source")
news_rankings = bias.column("Horizontal Rank")
news_dict = {}
for x in range(0, (len(news_sources))):
    news_dict[news_sources[x]] = news_rankings[x]


def weighter(currweight, source, rating):
    horirank = bias.where("News Source", source).column("Horizontal Rank").item(0)
    return currweight + (((rating - 5) / 10) * horirank)


def weight_from_mean(currweight, source):
    return abs((currweight + news_dict[source]) - 50)


def weightranker(currweight, top_news):
    for i in range(1, len(top_news)):
        if weight_from_mean(currweight, top_news[i]['id']) < weight_from_mean(currweight, top_news[i - 1]['id']):
            for j in range(i):
                if weight_from_mean(currweight, top_news[i]['id']) < weight_from_mean(currweight, top_news[j]['id']):
                    top_news[i], top_news[j] = top_news[j], top_news[i]
    return top_news[:5]


# a = [{'': 2, '': 1, '': 3, 'id': 'cnn'}, {'': 2, '': 1, '': 3, 'id': 'fortune'}, {'': 2, '': 1, '': 3, 'id': 'the-new-york-times'}]
# weightranker(50, a)
# print(a)
# for x in a:
#     print(news_dict[x['id']])
