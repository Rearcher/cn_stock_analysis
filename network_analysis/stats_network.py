import collections
import logging
import multiprocessing

import networkx as nx

from utils.date_util import get_date_ruler
from utils.log_util import log_config


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


def main():
    log_config('../logs/stat_network.txt')
    save_weight_avg_and_node_strength()
    pass


if __name__ == '__main__':
    main()
