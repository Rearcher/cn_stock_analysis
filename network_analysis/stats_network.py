import collections
import csv
import logging
import multiprocessing
import os

import community
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

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
    # date_ruler = get_date_ruler('2015-07-06', '2015-09-30')
    date_ruler = get_date_ruler('2015-01-06', '2015-11-02')
    strength_map = {}

    for date in date_ruler:
        filename = data_dir + 'shanghai_strength_' + str(date) + '.txt'
        with open(filename, 'r') as f:
            data = f.readlines()
            for line in data:
                line = line.strip('\n').split(' ')
                if line[0] in strength_map.keys():
                    strength_map[line[0]].append(float(line[1]))
                else:
                    strength_map[line[0]] = [float(line[1])]

    avg_strength_map = {}
    for k, v in strength_map.items():
        avg_strength_map[k] = sum(v) / len(v)

    avg_strength_map = collections.OrderedDict(sorted(avg_strength_map.items(), key=lambda x: x[1], reverse=True))
    for k, v in avg_strength_map.items():
        print(k, v)

    stock_num = '600016'
    with open('/Users/rahul/tmp/' + stock_num + '_strength.txt', 'w') as out:
        out.write('date strength\n')
        for i in range(0, len(date_ruler)):
            out.write(str(date_ruler[i]) + ' ' + str(strength_map[stock_num][i]) + '\n')

    pass


def community_analysis():
    data_dir = '/Users/rahul/tmp/data/graph_data/'
    filename = data_dir + 'shanghai_2015-07-27.gml'

    G = nx.read_gml(filename)
    threshold = 0.9
    for (u, v) in G.edges():
        if G[u][v]['weight'] < threshold:
            G.remove_edge(u, v)

    # nx.write_gml(G, '/Users/rahul/tmp/2015-07-28.0.9.gml')
    partition = community.best_partition(G)
    community_cnt = {}

    for k, v in partition.items():
        if v in community_cnt.keys():
            community_cnt[v].append(k)
        else:
            community_cnt[v] = [k]

    for k, v in community_cnt.items():
        print(k, len(v))

    sample = ['600051', '601798', '600016', '601398']
    for stock in sample:
        for k, v in community_cnt.items():
            if stock in v:
                print(stock, k)

    print(community_cnt[1])


def trending_analysis():
    data_dir = '/Users/rahul/tmp/data/aligned_data/'
    trading_map, transaction_map = {}, {}
    stocks = os.listdir(data_dir)
    date_ruler = list(map(str, get_date_ruler('2015-01-05', '2015-11-02')))

    begin_date, end_date = '2015-07-01', '2015-09-30'
    begin_idx, end_idx = date_ruler.index(begin_date), date_ruler.index(end_date)

    # print(begin_idx, end_idx)
    # print(date_ruler[begin_idx], date_ruler[end_idx])

    for i in range(begin_idx, end_idx + 1):
        trading_map[date_ruler[i]] = []
        transaction_map[date_ruler[i]] = []

    for stock in stocks:
        if not stock.startswith('60'):
            continue

        with open(data_dir + stock, 'r') as f:
            csv_reader = csv.DictReader(f)
            trading = [row['trading_volume'] for row in csv_reader]

            f.seek(0)
            csv_reader = csv.DictReader(f)
            transaction = [row['transaction_volume'] for row in csv_reader]

            for i in range(begin_idx, end_idx + 1):
                trading_map[date_ruler[i]].append(int(trading[i]))
                transaction_map[date_ruler[i]].append(float(transaction[i]))

    trading, transaction, weight_avg, sample_strength, date = [], [], [], [], []

    # get everyday's trading volume
    for k, v in trading_map.items():
        trading.append(sum(v))

    # get everyday's transaction volume
    for k, v in transaction_map.items():
        transaction.append(sum(v))

    # get everyday's average weight
    with open('/Users/rahul/tmp/weight_avg.txt', 'r') as f:
        csv_reader = csv.DictReader(f, delimiter=' ')
        weight_avg = [row['weight_avg'] for row in csv_reader]

        f.seek(0)
        csv_reader = csv.DictReader(f, delimiter=' ')
        date = [row['date'] for row in csv_reader]

        weight_avg = weight_avg[date.index(begin_date):(date.index(end_date) + 1)]

    # get stock 600051's everyday's strength
    with open('/Users/rahul/tmp/600051_strength.txt', 'r') as f:
        csv_reader = csv.DictReader(f, delimiter=' ')
        sample_strength = [row['strength'] for row in csv_reader]

        f.seek(0)
        csv_reader = csv.DictReader(f, delimiter=' ')
        date = [row['date'] for row in csv_reader]

        sample_strength = sample_strength[date.index(begin_date):(date.index(end_date) + 1)]

    # get date
    date = date[date.index(begin_date):(date.index(end_date) + 1)]
    date = list(map(lambda x:x[5:], date))

    ind = np.arange(len(date))
    f = '/System/Library/Fonts/STHeiti Medium.ttc'
    prop = fm.FontProperties(fname=f)

    plt.figure(1)
    plt.subplot(411)
    plt.plot(ind, sample_strength)
    plt.tick_params(axis='x', which='both', bottom='off', top='off', labelbottom='off')
    plt.ylabel('节点600051的强度', fontproperties=prop)
    plt.grid(True)
    plt.annotate('第一次救市', xy=(14, 600), fontproperties=prop)
    plt.annotate('第二次救市', xy=(48, 600), fontproperties=prop)
    plt.axvspan(xmin=date.index('07-06'), xmax=date.index('08-14'), color='green', alpha=0.2)
    plt.axvspan(xmin=date.index('08-26'), xmax=date.index('09-25'), color='green', alpha=0.2)

    plt.subplot(412)
    plt.plot(ind, weight_avg)
    plt.tick_params(axis='x', which='both', bottom='off', top='off', labelbottom='off')
    plt.ylabel('网络平均相关性', fontproperties=prop)
    plt.grid(True)
    plt.axvspan(xmin=date.index('07-06'), xmax=date.index('08-14'), color='green', alpha=0.2)
    plt.axvspan(xmin=date.index('08-26'), xmax=date.index('09-25'), color='green', alpha=0.2)

    plt.subplot(413)
    plt.plot(ind, transaction, color='red')
    plt.tick_params(axis='x', which='both', bottom='off', top='off', labelbottom='off')
    plt.ylabel('交易额', fontproperties=prop)
    plt.grid(True)
    plt.axvspan(xmin=date.index('07-06'), xmax=date.index('08-14'), color='green', alpha=0.2)
    plt.axvspan(xmin=date.index('08-26'), xmax=date.index('09-25'), color='green', alpha=0.2)

    plt.subplot(414)
    plt.plot(ind, trading, color='red')
    plt.xticks(ind, date, rotation='vertical')
    plt.ylabel('交易量', fontproperties=prop)
    plt.axvspan(xmin=date.index('07-06'), xmax=date.index('08-14'), color='green', alpha=0.2)
    plt.axvspan(xmin=date.index('08-26'), xmax=date.index('09-25'), color='green', alpha=0.2)
    plt.grid(True)

    plt.show()


def main():
    log_config('../logs/stat_network.txt')
    # save_weight_avg_and_node_strength()
    # show_weight_avg()
    # show_node_strength()
    # community_analysis()
    trending_analysis()
    pass


if __name__ == '__main__':
    main()
