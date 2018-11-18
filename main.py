from newsapi import NewsApiClient
from flask import Flask, url_for, render_template, request, jsonify
import weight

app = Flask(__name__)
newsapi = NewsApiClient(api_key='c38f8442c3f14c59acd996b41d7f4d4c')
sources = "cnn, the-new-york-times, bbc-news, the-guardian-uk, associated-press, usa-today, the-economist, the-hill, fortune, the-wall-street-journal"
sourcesarray = sources.split(", ")


def get_news_by_category(category):
    # top_economy = newsapi.get_top_headlines(q='economy', sources=sources)
    # top_politics = newsapi.get_top_headlines(q='politics', sources=sources)
    # top_sport = newsapi.get_top_headlines(q='sports', sources=sources)
    # top_tech = newsapi.get_top_headlines(q='technology', sources=sources)
    top_news = newsapi.get_top_headlines(q=category, sources=sources)

# categories = [top_economy, top_politics, top_sport, top_tech]
    final = []

# for x in categories:
    for x in top_news['articles']:
        final.append({'title': x['title'], 'url': x['url'], 'image': x['urlToImage'], 'id': x['source']['id']})
    return final


currweight = 50
def get_user_weight(source, rating):
    currweight = weight.weighter(currweight, source, rating)
    return currweight


# print(currweight)


a = get_news_by_category('politics')
for x in a:
    print(x)

@app.route("/", methods = ["GET"])
def home():
  pass

@app.route("/api/updateWeight")
def updateWeight():
  if request.method == "POST":
    source = request.form.get("source")
    user_rating = request.form.get("user_rating")

    return get_user_weight(source, user_rating)

@app.route("/api/getNews")
def getNews():
  if request.method == "POST":
    category = request.form.get("category")

    if (category):
      return jsonify(get_news_by_category(category))

if __name__ == "__main__":
  app.run(port = 5000)
