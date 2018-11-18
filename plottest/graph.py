import matplotlib.pyplot as plt
import matplotlib.style as style
import io
import base64
import numpy as np


def build_graph(source, avgscore):
    style.use('fivethirtyeight')
    plt.locator_params(integer=True)
    img = io.BytesIO()
    plt.tight_layout()
    plt.bar(source, avgscore, color='m')
    plt.xlabel('Source')
    plt.ylabel('Average Score Given')
    plt.title("Average Score Given per Source")
    plt.tight_layout()
    plt.ylim((0, 10))
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return 'data:image/png;base64,{}'.format(graph_url)
