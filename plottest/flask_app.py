import matplotlib.pyplot as plt
import io
import base64
from flask import Flask, render_template
from graph import build_graph

app = Flask(__name__)

@app.route('/')
def home()
    return "hello Jason"

@app.route('/graphs')
def graphs():
    # These coordinates could be stored in DB
    x1 = 5
    y1 = [10, 30, 40, 5, 50]
    x2 = 5
    y2 = [50, 30, 20, 10, 50]
    x3 = 5
    y3 = [0, 30, 10, 5, 30]

    graph1_url = build_graph(x1, y1)
    graph2_url = build_graph(x2, y2)
    graph3_url = build_graph(x3, y3)

    return render_template('graphs.html',
                           graph1=graph1_url,
                           graph2=graph2_url,
                           graph3=graph3_url)


if __name__ == '__main__':
    app.debug = True
    app.run(port=5000)
