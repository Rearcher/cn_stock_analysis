import collections
import numpy as np
import matplotlib.pyplot as plt

def main():
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


if __name__ == '__main__':
    main()
