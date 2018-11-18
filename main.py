from newsapi import NewsApiClient
from flask import Flask, url_for, render_template, request, jsonify, session
import weight, os


from datascience import Table
bias = Table().read_table("bias.csv").select("News Source", "Horizontal Rank")
news_sources = bias.column("News Source")
news_rankings = bias.column("Horizontal Rank")
news_dict = {}
for x in range(0, (len(news_sources))):
  news_dict[news_sources[x]] = news_rankings[x]


app = Flask(__name__)
newsapi = NewsApiClient(api_key='c38f8442c3f14c59acd996b41d7f4d4c')

# session.clear() (if need to clear session)

currentWeight = 50
sources = "cnn, the-new-york-times, bbc-news, the-guardian-uk, associated-press, usa-today, the-economist, the-hill, fortune"
sourcesarray = sources.split(", ")

def get_news_by_category(category):
  top_news = []
  if category == 'economy':
    top_news.append(newsapi.get_top_headlines(q='econ', sources=sources))
    top_news.append(newsapi.get_top_headlines(q='money', sources=sources))
    top_news.append(newsapi.get_top_headlines(q='monetary', sources=sources))
    top_news.append(newsapi.get_top_headlines(q='fiscal', sources=sources))
  if category == 'politics':
    top_news.append(newsapi.get_top_headlines(q='politic', sources=sources))
    top_news.append(newsapi.get_top_headlines(q='trump', sources=sources))
    top_news.append(newsapi.get_top_headlines(q='government', sources=sources))
  if category == 'world':
    top_news.append(newsapi.get_top_headlines(q='China', sources=sources))
    top_news.append(newsapi.get_top_headlines(q='Korea', sources=sources))
    top_news.append(newsapi.get_top_headlines(q='America', sources=sources))
    top_news.append(newsapi.get_top_headlines(q='Europe', sources=sources))
    top_news.append(newsapi.get_top_headlines(q='East', sources=sources))
    top_news.append(newsapi.get_top_headlines(q='Africa', sources=sources))
    top_news.append(newsapi.get_top_headlines(q='Mexico', sources=sources))
    top_news.append(newsapi.get_top_headlines(q='California', sources=sources))
  if category == 'technology':
    top_news.append(newsapi.get_top_headlines(q='tech', sources=sources))
    top_news.append(newsapi.get_top_headlines(q='Apple', sources=sources))
    top_news.append(newsapi.get_top_headlines(q='Google', sources=sources))
    top_news.append(newsapi.get_top_headlines(q='Amazon', sources=sources))
    top_news.append(newsapi.get_top_headlines(q='Facebook', sources=sources))
    top_news.append(newsapi.get_top_headlines(q='smart', sources=sources))
    top_news.append(newsapi.get_top_headlines(q='phone', sources=sources))
    top_news.append(newsapi.get_top_headlines(q='Silicon', sources=sources))
    top_news.append(newsapi.get_top_headlines(q='Samsung', sources=sources))


  final = []
  for y in top_news:
    for x in y['articles']:
      final.append({'title': x['title'], 'url': x['url'], 'image': x['urlToImage'], 'id': x['source']['id']})
  return weightranker(currentWeight, final)


def get_user_weight(source, rating, currWeight = 50):
  cWeight = weight.weighter(currWeight, source, rating)
  currentWeight = cWeight
  session["currentWeight"] = cWeight
  return currentWeight


def weight_from_mean(currweight, source):
  return abs((currweight + news_dict[source]) - 50)


def weightranker(currweight, top_news):  # when get_news_by_category is called, return value goes into this function at top_news
  for i in range(1, len(top_news)):
    if weight_from_mean(currweight, top_news[i]['id']) < weight_from_mean(currweight, top_news[i - 1]['id']):
      for j in range(i):
        if weight_from_mean(currweight, top_news[i]['id']) < weight_from_mean(currweight, top_news[j]['id']):
          top_news[i], top_news[j] = top_news[j], top_news[i]
  return top_news[:5]

@app.route("/")
def home():
  print(session.get("currentWeight"))
  return "hi"


@app.route("/api/updateWeight")
def updateWeight():
  if not ("currentWeight" in session):
    session["currentWeight"] = 50
  else:
    currentWeight = session["currentWeight"]

  if request.method == "GET":
    source = request.args.get("source")
    user_rating = request.args.get("user_rating")

  new_weight = get_user_weight(source, int(user_rating), currentWeight)
  session["currentWeight"] = new_weight
  return str(new_weight)


@app.route("/api/getNews")
def getNews():
  if not ("currentWeight" in session):
    session["currentWeight"] = 50
  else:
    currentWeight = session["currentWeight"]

  if request.method == "GET":
    category = request.args.get("category")

    if (category):
      return jsonify(get_news_by_category(category))

if __name__ == "__main__":
  app.secret_key = os.urandom(24)
  app.run(port=5001)
