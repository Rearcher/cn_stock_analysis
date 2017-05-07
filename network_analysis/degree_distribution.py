import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import multiprocessing
import logging
import collections

from utils.date_util import get_date_ruler
from utils.log_util import log_config


def get_degree_distribution(date, data_map, semaphore):
    data_dir = '/Users/rahul/tmp/data/all_graph_data/'
    G = nx.read_gml(data_dir + date + '.gml')
    edge_weights = [G[u][v]['weight'] for (u, v) in G.edges()]

    result = []
    for i in range(0, 10):
        result.append(0)
    for weight in edge_weights:
        if weight < 0:
            weight = 0
        if weight >= 1:
            weight = 0.99
        result[int(weight / 0.1)] += 1

    cnt = sum(result)
    for i in range(0, len(result)):
        result[i] = result[i] / cnt

    data_map[date] = result
    semaphore.release()


def save_degree_distribution():
    log_config('../logs/save_degree_distribution.log')

    concurrent_level = 6
    pool = multiprocessing.Pool(concurrent_level)
    manager = multiprocessing.Manager()
    semaphore = manager.Semaphore(concurrent_level)
    data_map = manager.dict()

    date_ruler = get_date_ruler('2015-01-06', '2015-11-02')
    for date in date_ruler:
        logging.info('processing ' + str(date) + '...')
        semaphore.acquire()
        pool.apply_async(get_degree_distribution, args=(str(date), data_map, semaphore))

    pool.close()
    pool.join()

    data_map = collections.OrderedDict(sorted(data_map.items()))
    logging.info('start saving...')
    with open('../resources/network_degree_distribution', 'w') as f:
        for k, v in data_map.items():
            f.write(k + ' ' + ' '.join(list(map(str, v))) + '\n')
    logging.info('complete.')


def show():
    with open('../resources/network_degree_distribution', 'r') as f:
        lines = f.readlines()
    lines = list(map(lambda x: x.strip('\n'), lines))

    data_map = {}
    for line in lines:
        line = line.split(' ')
        data_map[line[0]] = line[1:]

    data_map = collections.OrderedDict(sorted(data_map.items()))
    # series = []
    # for i in range(0, 10):
    #     series.append([])
    #
    # for k, v in data_map.items():
    #     for i in range(0, len(v)):
    #         series[i].append(v[i])

    series = [[], []]
    for k, v in data_map.items():
        series[0].append(sum(map(float, v[0:7])))
        series[1].append(sum(map(float, v[7:])))

    f = '/System/Library/Fonts/STHeiti Medium.ttc'
    prop = fm.FontProperties(fname=f)

    plt.figure()
    x = np.arange(0, 200)
    for i in range(0, len(series)):
        if i < 5:
            plt.plot(x, series[i], label=str(i))

    plt.legend(prop=prop, loc='upper right')
    plt.xticks(x, list(map(str, get_date_ruler('2015-01-06', '2015-11-02'))), rotation='vertical')
    plt.grid(True)
    plt.show()


def main():
    # save_degree_distribution()
    show()


if __name__ == '__main__':
    main()