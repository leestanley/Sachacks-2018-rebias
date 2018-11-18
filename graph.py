import matplotlib.pyplot as plt
import matplotlib.style as style
import io
import base64
import numpy as np


def build_graph(ratings, biasscore):
    style.use('fivethirtyeight')
    ratings = np.arange(0, ratings)
    plt.locator_params(integer=True)
    img = io.BytesIO()
    plt.tight_layout()
    plt.plot(ratings, biasscore, color='m')
    plt.xlabel('Amount of Ratings')
    plt.ylabel('Bias Score')
    plt.title("Ratings Plotted Against Bias Score")
    plt.tight_layout()
    plt.ylim((0, 100))
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return 'data:image/png;base64,{}'.format(graph_url)
