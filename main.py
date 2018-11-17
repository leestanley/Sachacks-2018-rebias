from newsapi import NewsApiClient
import weight

newsapi = NewsApiClient(api_key='c38f8442c3f14c59acd996b41d7f4d4c')
sources = "cnn, the-new-york-times, bbc-news, the-guardian-uk, associated-press, usa-today, the-economist, the-hill, fortune, the-wall-street-journal"
sourcesarray = sources.split(", ")

top_economy = newsapi.get_top_headlines(q='economy', sources=sources)
top_politics = newsapi.get_top_headlines(q='politics', sources=sources)
top_sport = newsapi.get_top_headlines(q='sports', sources=sources)
top_tech = newsapi.get_top_headlines(q='technology', sources=sources)

print(top_tech)
# print(weight.weighter("cnn", 7))
