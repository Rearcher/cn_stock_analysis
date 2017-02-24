import collections
import logging
import multiprocessing

import networkx as nx

from utils.date_util import get_date_ruler
from utils.log_util import log_config

import numpy as np
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt



def get_weight_avg_and_node_strength(semaphore, map, filename, date):

    G = nx.read_gml(filename)

    # save node strength
    outfile = '/Users/rahul/tmp/data/stats/' + 'shanghai_strength_' + date + '.txt'
    with open(outfile, 'w') as out:
        for k, v in G.degree(G.nodes(), weight='weight').items():
            out.write(k + ' ' + str(v) + '\n')

    edge_cnt = len(G.edges())
    weight_sum = sum(G[u][v]['weight'] for (u, v) in G.edges())
    map[date] = weight_sum / edge_cnt
    semaphore.release()


def save_weight_avg_and_node_strength():

    data_dir = '/Users/rahul/tmp/data/graph_data/'
    date_ruler = get_date_ruler('2015-01-06', '2015-11-02')

    concurrent_level = 4
    pool = multiprocessing.Pool(concurrent_level)
    manager = multiprocessing.Manager()
    semaphore = manager.Semaphore(concurrent_level)
    map = manager.dict()

    for date in date_ruler:
        semaphore.acquire()
        logging.info('processing... date = %s', str(date))
        filename = data_dir + 'shanghai_' + str(date) + '.gml'
        pool.apply_async(get_weight_avg_and_node_strength, args=(semaphore, map, filename, str(date)))

    pool.close()
    pool.join()

    map = collections.OrderedDict(sorted(map.items()))

    logging.info('saving weight average...')
    with open('/Users/rahul/tmp/data/stats/weight_avg.txt', 'w') as out:
        for k, v in map.items():
            out.write(k + ' ' + str(v) + '\n')

    pass


def show_weight_avg():

    date, weight_avg = [], []
    with open('/Users/rahul/tmp/data/stats/weight_avg.txt', 'r') as f:
        data = f.readlines()
        for line in data:
            line = line.strip('\n')
            line = line.split(' ')
            date.append(line[0])
            weight_avg.append(float(line[1]))

    begin_idx = date.index('2015-07-06')
    end_idx = date.index('2015-09-30')
    date = date[begin_idx:end_idx]
    weight_avg = weight_avg[begin_idx:end_idx]

    N = len(date)
    f = '/System/Library/Fonts/STHeiti Medium.ttc'
    prop = fm.FontProperties(fname=f)

    ind, width = np.arange(N), 0.35
    plt.bar(ind, weight_avg, width)

    plt.ylabel('网络平均相关性', fontproperties=prop)
    plt.title('网络平均相关性统计图', fontproperties=prop)
    plt.xticks(ind, date, rotation='vertical')
    plt.ylim(0.4, 0.7)
    plt.show()


def show_node_strength():
    data_dir = '/Users/rahul/tmp/data/stats/'
    date_ruler = get_date_ruler('2015-01-06', '2015-11-02')
    pass


def main():
    log_config('../logs/stat_network.txt')
    # save_weight_avg_and_node_strength()
    show_weight_avg()
    pass


if __name__ == '__main__':
    main()
