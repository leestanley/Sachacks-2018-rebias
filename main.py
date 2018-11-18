from newsapi import NewsApiClient
from flask import Flask, url_for, render_template, request, jsonify, session
import weight

app = Flask(__name__)
newsapi = NewsApiClient(api_key='c38f8442c3f14c59acd996b41d7f4d4c')

# session.clear() (if need to clear session)
app.secret_key = "f6438f71864f3da4caa96d2dfe804edb"

sources = "cnn, the-new-york-times, bbc-news, the-guardian-uk, associated-press, usa-today, the-economist, the-hill, fortune, the-wall-street-journal"
sourcesarray = sources.split(", ")
currWeight = 50
if session["currWeight"]:
    currWeight = session["currWeight"]
    print("session loaded")

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
    # top_news = newsapi.get_top_headlines(q=category, sources=sources)

# categories = [top_economy, top_politics, top_sport, top_tech]
    final = []

# for x in categories:
    for y in top_news:
        for x in y['articles']:
            final.append({'title': x['title'], 'url': x['url'], 'image': x['urlToImage'], 'id': x['source']['id']})
    return final


def get_user_weight(source, rating):
    currWeight = weight.weighter(currWeight, source, rating)
    session["currWeight"] = currWeight
    return currWeight

@app.before_request
def pre_session():
    session.permanent = True

@app.route("/", methods = ["GET"])
def home():
  pass

@app.route("/api/updateWeight")
def updateWeight():
  if request.method == "GET":
    source = request.args.get("source")
    user_rating = request.args.get("user_rating")

    return get_user_weight(source, user_rating)

@app.route("/api/getNews")
def getNews():
  if request.method == "GET":
    category = request.args.get("category")

    if (category):
      return jsonify(get_news_by_category(category))

if __name__ == "__main__":
  app.run(port = 5001)
