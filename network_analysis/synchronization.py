import collections
import logging
import multiprocessing

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from utils.data_util import read_data
from utils.date_util import get_date_ruler
from utils.log_util import log_config


def get_synchronization(date, semaphore, map):
    data_dir = '/Users/rahul/tmp/data/all_graph_data/'
    G = nx.read_gml(data_dir + date + '.gml')
    result = sum([G[u][v]['weight'] for (u, v) in G.edges()]) / len(G.edges())
    map[date] = result
    semaphore.release()


def save_synchronization():
    log_config('../logs/sava_sync.log')
    date_ruler = get_date_ruler('2015-01-06', '2015-11-02')

    concurrent_level = 6
    pool = multiprocessing.Pool(concurrent_level)
    manager = multiprocessing.Manager()
    semaphore = manager.Semaphore(concurrent_level)
    map = manager.dict()

    for date in date_ruler:
        logging.info('processing ' + str(date) + '...')
        semaphore.acquire()
        pool.apply_async(get_synchronization, args=(str(date), semaphore, map))

    pool.close()
    pool.join()

    map = collections.OrderedDict(sorted(map.items()))
    with open('../resources/synchronization.txt', 'w') as f:
        for k, v in map.items():
            f.write(str(v) + '\n')


def show_synchronization():
    begin_date, end_date = '2015-01-06', '2015-11-02'
    y = read_data(data_dir='../resources/', file='synchronization.txt', begin_date=begin_date, end_date=end_date)
    x = list(map(lambda x: str(x)[5:], get_date_ruler(begin_date=begin_date, end_date=end_date)))

    s, t = x.index('01-06'), x.index('11-02')

    ind = np.arange(len(x[s:(t+1)]))
    f = '/System/Library/Fonts/STHeiti Medium.ttc'
    prop = fm.FontProperties(fname=f)

    plt.plot(ind, y[s:(t+1)])
    plt.xlabel('日期', fontproperties=prop)
    plt.ylabel('网络同步性', fontproperties=prop)
    plt.axvspan(xmin=x.index('06-15'), xmax=x.index('07-06'), color='red', alpha=0.2)
    plt.axvspan(xmin=x.index('07-06'), xmax=x.index('09-30'), alpha=0.2)
    plt.annotate('救市期', xy=(300, 500), fontproperties=prop)
    plt.xticks(ind, x[s:(t+1)], rotation='vertical', fontsize=5)
    plt.show()


def main():
    # save_synchronization()
    show_synchronization()


if __name__ == '__main__':
    main()
