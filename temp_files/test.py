import networkx as nx
import traceback
import os

from utils.date_util import get_date_ruler


def get_correlation(filename, idx):
    with open(filename, 'r') as f:
        cors = f.readlines()
        cors = [round(float(cor), 2) for cor in cors]
    return cors[idx]


def save_graph(stocks, data_dir, output_dir, date_ruler, idx):
    # G = nx.DiGraph()
    G = nx.Graph()
    for i in range(0, len(stocks) - 1):
        for j in range(i + 1, len(stocks)):
            filename = 'cor_' + stocks[i] + '_' + stocks[j]
            try:
                cor = get_correlation(data_dir + filename, idx)
                if cor < 0.85:
                    continue
                G.add_edge(stocks[i], stocks[j], weight=cor)
                # G.add_edge(stocks[j], stocks[i], weight=cor)
            except:
                traceback.print_exc()

    print('start saving to disk...')
    nx.write_gml(G, output_dir + 'test.gml')


def main():
    save_graph(stocks, data_dir, output_dir, date_ruler, 0)
    pass


if __name__ == '__main__':

    data_dir = '/Users/rahul/tmp/correlations/'
    stock_dir = '/Users/rahul/tmp/data/aligned_data/'
    output_dir = '/Users/rahul/tmp/'

    # acquire stock list and date ruler
    stocks = list(map(lambda x: x[:6], filter(lambda stock: stock.startswith('60'), os.listdir(stock_dir))))
    date_ruler = get_date_ruler('2015-01-06', '2015-11-02')

    main()
