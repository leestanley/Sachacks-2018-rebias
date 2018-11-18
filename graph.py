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
    bar1 = plt.bar(source, avgscore, width=0.35, color='m', align='center')
    plt.xlabel('Source')
    plt.ylabel('Average Score Given')
    plt.title("Average Score Given per Source")
    plt.tight_layout()
    plt.ylim((0, 10))
    for bar in bar1:
        height = bar.get_height()
        plt.text(bar.get_x()+ (0.35/2), height, '%d' % float(height), ha='center', va='bottom')
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return 'data:image/png;base64,{}'.format(graph_url)
