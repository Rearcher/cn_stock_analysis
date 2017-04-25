import logging
import multiprocessing
import os
import traceback

import networkx as nx

from utils.date_util import get_date_ruler
from utils.log_util import log_config


def get_correlation(filename, idx):
    with open(filename, 'r') as f:
        cors = f.readlines()
        cors = [round(float(cor), 2) for cor in cors]
    return cors[idx]


def save_graph(semaphore, stocks, data_dir, output_dir, date_ruler, idx):
    G = nx.Graph()
    for i in range(0, len(stocks) - 1):
        for j in range(i + 1, len(stocks)):
            filename = 'cor_' + stocks[i] + '_' + stocks[j]
            try:
                cor = get_correlation(data_dir + filename, idx)
                G.add_edge(stocks[i], stocks[j], weight=cor)
            except:
                traceback.print_exc()

    nx.write_gml(G, output_dir + str(date_ruler[idx]) + '.gml')
    semaphore.release()


def main():
    # log file config
    log_config('../logs/save_graph.log')

    # directory config
    data_dir = '/Users/rahul/tmp/correlations/'
    stock_dir = '/Users/rahul/tmp/data/aligned_data/'
    output_dir = '/Users/rahul/tmp/data/all_graph_data/'

    # acquire stock list and date ruler
    stocks = list(map(lambda x: x[:6], filter(lambda stock: stock.startswith('60') or stock.startswith('000'), os.listdir(stock_dir))))
    date_ruler = get_date_ruler('2015-01-06', '2015-11-02')

    # multiprocessing, use semaphore to control concurrent
    concurrent_level = 8
    pool = multiprocessing.Pool(concurrent_level)
    manager = multiprocessing.Manager()
    semaphore = manager.Semaphore(concurrent_level)
    for i in range(10, len(date_ruler)):
        semaphore.acquire()
        logging.info('processing index=%s, date=%s', i, str(date_ruler[i]))
        pool.apply_async(save_graph, args=(semaphore, stocks, data_dir, output_dir, date_ruler, i))
    pool.close()
    pool.join()

if __name__ == '__main__':
    main()
