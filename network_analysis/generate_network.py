import os
import traceback

import networkx as nx
import matplotlib.pyplot as plt
from utils.date_util import get_date_ruler
from networkx.drawing.nx_pydot import write_dot
from networkx.drawing.nx_agraph import graphviz_layout



def get_correlation(filename):
    input_file = open(filename, 'r')
    cors = input_file.readlines()
    cors = [round(float(cor), 2) for cor in cors]
    input_file.close()
    return cors[0]


def generate_from_cor():
    data_dir = '/Users/rahul/tmp/correlations/'
    stocks = []
    for stock in os.listdir('/Users/rahul/tmp/data/aligned_data'):
        if stock.startswith('.') or stock.startswith('002') or stock.startswith('300'):
            continue
        stocks.append(stock[:6])

    stocks = stocks[:10]
    G = nx.Graph()
    for i in range(0, len(stocks)-1):
        for j in range(i+1, len(stocks)):
            filename = 'cor_' + stocks[i] + '_' + stocks[j]
            try:
                G.add_edge(stocks[i], stocks[j], weight=get_correlation(data_dir + filename))
            except:
                traceback.print_exc()

    print(G.nodes())
    # nodes = nx.draw_networkx_nodes(G, pos=nx.spring_layout(G))
    # plt.show()
    nx.draw(G, pos=graphviz_layout(G))
    plt.show()


def main():
    data_dir = '/Users/rahul/tmp/correlations'
    # files = os.listdir(data_dir)
    # print(len(files))
    # G = nx.Graph()
    # G.add_edge('000001', '000002', weight=0.8)
    # G.add_edge('000001', '000003', weight=0.4)
    # print(G.edges(data='weight'))
    # print(G.nodes())
    generate_from_cor()
    # print(get_correlation(data_dir + '/cor_603997_603998'))


if __name__ == '__main__':
    main()
