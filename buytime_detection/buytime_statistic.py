import collections
import numpy as np
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

def stats():

    # key = date
    # value = [[stocks], blue_trade_num_cnt, blue_trade_money_cnt, simple_trade_num_cnt, simple_trade_money_cnt]
    # store all in map
    map = {}
    input = open('../logs/buytime_2.log')
    line = input.readline()
    while line:
        line, i = line.strip('\n').split(' '), 1
        stock_num = line[0]

        while i < len(line):
            current_date, current_trade_num, current_trade_money = line[i], int(line[i + 1]), float(line[i + 2])
            if current_date in map.keys():
                map[current_date][0].append(stock_num)
                # judge if it is blue stock
                if stock_num.startswith('60') or stock_num.startswith('000'):
                    map[current_date][1] += current_trade_num
                    map[current_date][2] += current_trade_money
                else:
                    map[current_date][3] += current_trade_num
                    map[current_date][4] += current_trade_money
            else:
                map[line[i]] = [[], 0, 0, 0, 0]
            i += 3

        line = input.readline()
    input.close()

    # start to process map
    x_name, blue_cnt, simple_cnt = [], [], []
    blue_trade_num, blue_trade_money = [], []
    simple_trade_num, simple_trade_money = [], []
    map = collections.OrderedDict(sorted(map.items()))
    for k, v in map.items():
        current_blue_cnt, current_simple_cnt = 0, 0
        for stock_num in v[0]:
            if stock_num.startswith('60') or stock_num.startswith('000'):
                current_blue_cnt += 1
            else:
                current_simple_cnt += 1
        x_name.append(k)
        blue_cnt.append(current_blue_cnt)
        simple_cnt.append(current_simple_cnt)
        blue_trade_num.append(v[1])
        blue_trade_money.append(v[2])
        simple_trade_num.append(v[3])
        simple_trade_money.append(v[4])

    # data visualization
    N = len(x_name)
    f = '/System/Library/Fonts/STHeiti Medium.ttc'
    prop = fm.FontProperties(fname=f)

    ind, width = np.arange(N), 0.35
    p1 = plt.bar(ind, blue_cnt, width, color='blue', label='blue')
    p2 = plt.bar(ind, simple_cnt, width, color='red', bottom=blue_cnt, label='simple')


    plt.ylabel('交易额', fontproperties=prop)
    plt.title('交易额统计', fontproperties=prop)
    # plt.ylabel('股票数', fontproperties=prop)
    # plt.title('股票买入数统计', fontproperties=prop)
    plt.xticks(ind, x_name, rotation='vertical')
    # plt.legend((p1[0], p2[0]), ('蓝筹股', '中小股'))
    plt.legend()
    plt.show()




def old_main():
    map = {}
    input = open('../logs/buytime_2.log')
    line = input.readline()
    while line:
        line = line.strip('\n').split(' ')
        for i in range(1, len(line)):
            if line[i] in map.keys():
                map[line[i]].append(line[0])
            else:
                map[line[i]] = []
        line = input.readline()

    input.close()

    xname, blue_cnt, simple_cnt = [], [], []
    map = collections.OrderedDict(sorted(map.items()))
    for k, v in map.items():
        blue_stock, simple_stock = 0, 0
        for stock in v:
            if stock.startswith('60') or stock.startswith('000'):
                blue_stock += 1
            else:
                simple_stock += 1
        xname.append(k)
        blue_cnt.append(blue_stock)
        simple_cnt.append(simple_stock)

    N = len(xname)
    ind = np.arange(N)
    width = 0.35
    p1 = plt.bar(ind, blue_cnt, width)
    p2 = plt.bar(ind, simple_cnt, width, color='#d62728', bottom=blue_cnt)
    plt.ylabel('Number of stocks')
    plt.title('Stock daily')
    plt.xticks(ind, xname, rotation='vertical')
    plt.legend((p1[0], p2[0]), ('Blue Stock', 'Simple Stock'))
    plt.show()
    pass


def main():
    stats()


if __name__ == '__main__':
    main()
