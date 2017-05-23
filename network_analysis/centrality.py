import logging
import multiprocessing

import collections
import community
import networkx as nx
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

from utils.date_util import get_date_ruler
from utils.log_util import log_config
from save_market_analysis.save_market import get_classification_list
from save_market_analysis.save_market import draw_pie
from save_market_analysis.save_market import get_index_data


def cal_properties(date, threshold, semaphore):
    data_dir = '/Users/rahul/tmp/data/all_graph_data/'
    G = nx.read_gml(data_dir + date + '.gml')

    for (u, v) in G.edges():
        if G[u][v]['weight'] < threshold:
            G.remove_edge(u, v)

    output_dir = '/Users/rahul/tmp/data/0_9/'
    dc_dir, cc_dir, bc_dir = output_dir + 'dc/', output_dir + 'cc/', output_dir + 'bc/'
    partition_dir = output_dir + 'partition/'

    dc, cc, bc = nx.degree_centrality(G), nx.closeness_centrality(G), nx.betweenness_centrality(G)
    partition = community.best_partition(G)

    with open(dc_dir + date, 'w') as f:
        for k, v in dc.items():
            f.write(k + ' ' + str(v) + '\n')
    with open(cc_dir + date, 'w') as f:
        for k, v in cc.items():
            f.write(k + ' ' + str(v) + '\n')
    with open(bc_dir + date, 'w') as f:
        for k, v in bc.items():
            f.write(k + ' ' + str(v) + '\n')
    with open(partition_dir + date, 'w') as f:
        for k, v in partition.items():
            f.write(k + ' ' + str(v) + '\n')

    nx.betweenness_centrality()
    semaphore.release()


def save():
    log_config('../logs/centrality.log')
    date_ruler = get_date_ruler('2015-01-06', '2015-11-02')

    concurrent_level = 3
    pool = multiprocessing.Pool(concurrent_level)
    manager = multiprocessing.Manager()
    semaphore = manager.Semaphore(concurrent_level)

    threshold = 0.9
    for date in date_ruler:
        semaphore.acquire()
        logging.info('processing ' + str(date) + '...')
        pool.apply_async(cal_properties, args=(str(date), threshold, semaphore))

    pool.close()
    pool.join()
    logging.info('complete.')


def get_buy_stock():
    with open('../resources/national_team_investment.csv', 'r') as f:
        lines = f.readlines()
    lines = list(map(lambda x: x.strip('\n').split(',')[1], lines))
    return list(filter(lambda x: x.startswith('000') or x.startswith('60'), lines))


def centrality_analysis(data_dir):
    buy_stock = get_buy_stock()
    date_ruler = list(map(str, get_date_ruler('2015-01-06', '2015-11-02')))
    save_begin, save_end = date_ruler.index('2015-07-06'), date_ruler.index('2015-09-30')
    result = {}

    for stock in buy_stock:
        rank, centrality = [], []
        for date in date_ruler:
            file = data_dir + str(date)
            with open(file, 'r') as f:
                lines = f.readlines()
            lines = list(map(lambda x: x.strip('\n').split(' '), lines))

            data_map = {}
            for line in lines:
                data_map[line[0]] = float(line[1])

            if stock not in data_map.keys():
                break

            data_map = collections.OrderedDict(sorted(data_map.items(), key=lambda x: x[1], reverse=True))
            centrality.append(data_map[stock])
            rank.append(list(data_map.keys()).index(stock))

        if len(rank) == 0 or len(centrality) == 0:
            print(stock + ' not allowed.')
            continue

        rank_1, rank_2, rank_3 = sum(rank[:save_begin]) / save_begin, \
                                 sum(rank[save_begin:(save_end+1)]) / (save_end - save_begin), \
                                 sum(rank[save_end:]) / (len(rank) - save_end)
        if rank_2 < rank_1 and rank_2 < rank_3:
            result[stock] = rank_2

    result = collections.OrderedDict(sorted(result.items(), key=lambda x:x[1]))
    # print(len(result.keys()), list(result.keys()))
    # print(len(result.values()), list(result.values()))
    # print(get_classification_list(list(result.keys()), classification_type='concept'))
    return result

    # plt.figure(1)
    #
    # plt.subplot(211)
    # plt.plot(np.arange(0, len(rank)), rank)
    #
    # plt.subplot(212)
    # plt.plot(np.arange(0, len(centrality)), centrality)
    #
    # plt.show()


def community_analysis(data_dir):
    date_ruler = get_date_ruler('2015-01-06', '2015-11-02')
    community_cnt, community_member_cnt = [], []
    community_member = []

    for date in date_ruler:
        file = data_dir + str(date)
        with open(file, 'r') as f:
            lines = f.readlines()
        lines = list(map(lambda x: x.strip('\n').split(' '), lines))

        data_map = {}
        for line in lines:
            if line[1] in data_map.keys():
                data_map[line[1]].append(line[0])
            else:
                data_map[line[1]] = [line[0]]

        community_cnt.append(len(data_map.keys()))
        community_member_cnt.append(max(map(lambda x: len(x), list(data_map.values()))))

        data_map = collections.OrderedDict(sorted(data_map.items(), key=lambda x: len(x[1]), reverse=True))
        community_member.append(list(data_map.values())[0])


    # f = '/System/Library/Fonts/STHeiti Medium.ttc'
    f = '/Users/rahul/Library/Fonts/simsun.ttf'
    prop = fm.FontProperties(fname=f)
    x = list(map(lambda x: str(x)[5:], date_ruler))
    for i in range(0, len(x)):
        if i % 5 != 0:
            x[i] = ''

    plt.figure(1)
    plt.subplot(211)
    plt.plot(np.arange(0, len(community_cnt)), community_cnt)
    plt.ylabel('社团数', fontproperties=prop)
    # plt.grid(True)

    plt.subplot(212)
    plt.plot(np.arange(0, len(community_member_cnt)), community_member_cnt, color='red')
    plt.ylabel('最大社团成员数', fontproperties=prop)
    plt.xlabel('日期', fontproperties=prop)

    plt.xticks(np.arange(0, len(date_ruler)), x, rotation='vertical')
    # plt.grid(True)
    plt.show()
    #
    # key_map = {}
    # for x in community_member:
    #     classification_map = get_classification_list(x, classification_type='area')
    #     classification_map = collections.OrderedDict(sorted(classification_map.items(), key=lambda x:len(x[1]), reverse=True))
    #     for key in classification_map.keys():
    #         if key in key_map.keys():
    #             key_map[key] += len(classification_map[key])
    #         else:
    #             key_map[key] = len(classification_map[key])
    #
    # key_map = collections.OrderedDict(sorted(key_map.items(), key=lambda x:x[1], reverse=True))
    # for k, v in key_map.items():
    #     print(k, v)
    # pass


def get_max_community(date):
    community_map = {}
    data_dir = '/Users/rahul/tmp/data/0_9/partition/'

    with open(data_dir + date, 'r') as f:
        lines = f.readlines()
        lines = map(lambda x: x.strip('\n').split(' '), lines)

        for line in lines:
            if line[1] in community_map.keys():
                community_map[line[1]].append(line[0])
            else:
                community_map[line[1]] = [line[0]]

    community_map = collections.OrderedDict(sorted(community_map.items(), key=lambda x:len(x[1]), reverse=True))
    return list(community_map.values())[0]


def special_analysis():
    max_1 = get_max_community('2015-07-27')
    max_2 = get_max_community('2015-07-28')
    # max_1, max_2 = get_max_community('2015-08-18'), get_max_community('2015-08-19')
    buy_stock = get_buy_stock()

    in_buy = [val for val in max_2 if val in buy_stock]
    out_buy = [val for val in max_2 if val not in buy_stock]

    print(len(in_buy), in_buy)
    print(len(out_buy), out_buy)

    type = 'industry'
    draw_pie(get_classification_list(in_buy, classification_type=type))
    draw_pie(get_classification_list(out_buy, classification_type=type))


def get_buy_stock_until(date):
    result = set()
    with open('../resources/time_to_stock', 'r') as f:
        lines = f.readlines()
        lines = list(map(lambda x: x.strip('\n').split(' '), lines))
        for line in lines:
            if line[0] <= date:
                for i in range(1, len(line)):
                    result.add(line[i])
    return list(result)


def community_component_analysis():
    with open('../resources/time_to_stock', 'r') as f:
        lines = f.readlines()
        lines = list(map(lambda x: x.strip('\n').split(' '), lines))

    dates = list(map(lambda x: x[0], lines))
    y1, y2 = [], []
    for i in range(0, len(dates)):
        max_community = get_max_community(dates[i])
        # buy_stock = lines[i][1:]
        buy_stock = get_buy_stock_until(dates[i])

        in_buy = [val for val in max_community if val in buy_stock]
        out_buy = [val for val in max_community if val not in buy_stock]

        print(dates[i], len(in_buy), len(out_buy), len(out_buy) / len(max_community))
        y1.append(len(out_buy))
        y2.append(len(out_buy) / len(max_community))

    ind = np.arange(0, len(dates))
    plt.figure(1)

    plt.subplot(211)
    plt.plot(ind, y1)
    plt.grid(True)

    plt.subplot(212)
    plt.plot(ind, y2)
    plt.xticks(ind, dates, rotation='vertical')
    plt.grid(True)
    plt.show()


def community_component_analysis_2():
    begin_date, end_date = '2015-07-06', '2015-09-30'
    date_ruler = get_date_ruler(begin_date, end_date)

    y1, y2 = [], []
    for date in date_ruler:
        max_community = get_max_community(str(date))
        buy_stock = get_buy_stock_until(str(date))
        y1.append(len([val for val in max_community if val not in buy_stock]) / len(max_community))
        y2.append(len([val for val in max_community if val not in buy_stock]))

    _1, _2, _3 = get_index_data('399300')
    y3 = _2[_1.index(begin_date):(_1.index(end_date)+1)]
    y4 = _3[_1.index(begin_date):(_1.index(end_date)+1)]

    print(np.corrcoef(y1, y3))
    print(np.corrcoef(y1, y4))
    print(np.corrcoef(y3, y4))

    # f = '/System/Library/Fonts/STHeiti Medium.ttc'
    f = '/Users/rahul/Library/Fonts/simsun.ttf'
    prop = fm.FontProperties(fname=f)
    ind = np.arange(0, len(date_ruler))
    plt.figure()

    plt.plot(ind, y1)
    # plt.grid(True)
    plt.xticks(ind, list(map(lambda x: str(x)[5:], date_ruler)), rotation='vertical')
    plt.xlabel('日期', fontproperties=prop)
    plt.ylabel('非调控对象所占比例', fontproperties=prop)
    plt.show()

    pass


def main():
    # save()
    # centrality_analysis(data_dir='/Users/rahul/tmp/data/0_9/dc/')
    # community_analysis(data_dir='/Users/rahul/tmp/data/0_9/partition/')
    with open('/Users/rahul/tmp/data/dc_result.txt', 'r') as f:
        lines = f.readlines()
        lines = list(map(lambda x: x.strip('\n').split(' '), lines))
        dc_map = {}
        for line in lines:
            dc_map[line[0]] = line[1]

    with open('/Users/rahul/tmp/data/bc_result.txt', 'r') as f:
        lines = f.readlines()
        lines = list(map(lambda x: x.strip('\n').split(' '), lines))
        bc_map = {}
        for line in lines:
            bc_map[line[0]] = line[1]

    c1 = list(dc_map.keys())
    c2 = list(bc_map.keys())
    c3 = [val for val in c1 if val in c2]

    classification_list = get_classification_list(c3, classification_type='industry')
    for k, v in classification_list.items():
        print(k, v, '\n')
    print(c3)
    draw_pie(classification_list)


if __name__ == '__main__':
    # print(len(get_buy_stock()))
    main()
    # community_analysis('/Users/rahul/tmp/data/0_9/partition/')
    # special_analysis()
    # community_component_analysis_2()