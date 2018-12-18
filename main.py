from newsapi import NewsApiClient
from flask import Flask, url_for, render_template, request, jsonify, session
import weight, os, menuScraping, graph, weightranking
from datetime import datetime
from datascience import Table

import matplotlib.pyplot as plt
import io
import base64
from graph import build_graph

bias = Table().read_table("bias.csv").select("News Source", "Horizontal Rank")
news_sources = bias.column("News Source")
news_rankings = bias.column("Horizontal Rank")
news_dict = {}
for x in range(0, (len(news_sources))):
  news_dict[news_sources[x]] = news_rankings[x]


app = Flask(__name__)
newsapi = NewsApiClient(api_key='672b5745f9aa4ecbbc044a0025fc28d3')

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
    if (not (y['articles'] is None)):
      for x in excludeList(y['articles'], session.get("doneList")):
        final.append({'title': x['title'], 'url': x['url'], 'image': x['urlToImage'], 'id': x['source']['id'], 'content': x['content']})
  
  return weightranker(session["currentWeight"], final)


def get_user_weight(source, rating, currWeight = 50):
  cWeight = weight.weighter(currWeight, source, rating)
  session["currentWeight"] = cWeight
  return session["currentWeight"]

def weight_from_mean(currweight, source):
  return abs((currweight + news_dict[source]) - 50)

def excludeList(original, exclude):
  if (exclude is None):
    return original
  else:
    new_list = []

    for item in original:
      if not (item['url'] in exclude):
        new_list.append(item)
    
    return new_list
  
    

def weightranker(currweight, top_news):  # when get_news_by_category is called, return value goes into this function at top_news
  for i in range(1, len(top_news)):
    if weight_from_mean(currweight, top_news[i]['id']) < weight_from_mean(currweight, top_news[i - 1]['id']):
      for j in range(i):
        if weight_from_mean(currweight, top_news[i]['id']) < weight_from_mean(currweight, top_news[j]['id']):
          top_news[i], top_news[j] = top_news[j], top_news[i]
  return top_news[:8]

def checkSession():
  if not ("startUp" in session):
    session["startUp"] = datetime.today()
  else:
    if ((datetime.today() - session["startUp"]).days > 2):
      session.clear()
      session["startUp"] = datetime.today()
    
  if not ("currentWeight" in session):
    session["currentWeight"] = 50
  
  if not ("doneList" in session):
    session["doneList"] = []
  
  if not ("srcdict" in session):
    session["srcdict"] = {}

@app.route("/")
def home():
  return render_template("index.html")


@app.route("/api/updateWeight")
def updateWeight():
  checkSession()

  if request.method == "GET":
    url = request.args.get("url")
    source = request.args.get("source")
    user_rating = request.args.get("user_rating")
    
    new_weight = get_user_weight(source, int(user_rating), session.get("currentWeight"))
    session["currentWeight"] = new_weight

    oldDone = session["doneList"].copy()
    oldDone.append(url)
    session["doneList"] = oldDone

    newDict = weightranking.update_dict(session["srcdict"], source, user_rating)
    session["srcdict"] = newDict

    return str(new_weight)


@app.route("/api/getNews")
def getNews():
  checkSession()

  if request.method == "GET":
    category = request.args.get("category")

    if (category):
      return jsonify(get_news_by_category(category))

@app.route("/api/scrapText")
def scrapText():
  checkSession()

  if request.method == "GET":
    articleUrl = request.args.get("articleUrl")

    if (articleUrl):
      return menuScraping.getSoup(articleUrl)

@app.route("/api/getWeight")
def getWeight():
  checkSession()

  if request.method == "GET":
    return str(session["currentWeight"])

@app.route('/graph1')
def graph1():
    checkSession()

    source_biases = weightranking.source_user_biases(session["srcdict"])
    x1 = []
    y1 = []
    for x in source_biases:
      x1.append(x[0])
      y1.append(x[1])
    graph1_url = graph.build_graph(x1, y1)
    
    if request.method == "GET":
      return render_template('graph.html',
                           graph1=graph1_url)

if __name__ == "__main__":
  app.secret_key = os.urandom(24)
  app.run(port=6792)