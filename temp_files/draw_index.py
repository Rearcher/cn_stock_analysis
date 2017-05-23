from utils.data_util import read_raw_data
from utils.data_util import read_data
import matplotlib
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np


def draw_index():
    data_dir = '/Users/rahul/tmp/index_data/'
    shanghai = '000001.csv'
    shenzhen = '399106.csv'
    hs300 = '399300.csv'

    begin_date, end_date = '2015-01-06', '2015-11-02'
    (date, shanghai_close) = read_raw_data(data_dir, file=shanghai, begin_date=begin_date, end_date=end_date, columns=['close'], delimiter=' ')
    (date, shenzhen_close) = read_raw_data(data_dir, file=shenzhen, begin_date=begin_date, end_date=end_date, columns=['close'], delimiter=' ')
    (date, hs300_close) = read_raw_data(data_dir, file=hs300, begin_date=begin_date, end_date=end_date, columns=['close'], delimiter=' ')

    ind = np.arange(len(date))
    # f = '/System/Library/Fonts/STHeiti Medium.ttc'
    f = '/Users/rahul/Library/Fonts/simsun.ttf'
    prop = fm.FontProperties(fname=f)
    date = list(map(lambda x: x[5:], date))
    for i in range(0, 200):
        if (i+1) % 10 != 0:
            date[i] = ''

    fig = plt.figure(1)
    plt.plot(ind, shanghai_close[0], label='上证综指')
    plt.plot(ind, shenzhen_close[0], label='深证综指')
    plt.plot(ind, hs300_close[0], label='沪深300')
    plt.xticks(ind, date, rotation='vertical', fontsize=5)
    plt.legend(prop=prop, loc='upper right')
    plt.xlabel('日期', fontproperties=prop)
    plt.ylabel('指数', fontproperties=prop)
    # plt.grid(True)
    # plt.gcf().autofmt_xdate()

    plt.show()


def draw_trading_volume():
    data_dir = '/Users/rahul/tmp/data/aligned_data/'

    begin_date, end_date = '2015-07-01', '2015-09-30'
    (date, trading) = read_raw_data(data_dir, '601318.txt', begin_date=begin_date, end_date=end_date, columns=['trading_volume'])

    ind = np.arange(len(date))
    # f = '/System/Library/Fonts/STHeiti Medium.ttc'
    f = '/Users/rahul/Library/Fonts/simsun.ttf'
    prop = fm.FontProperties(fname=f)
    date = list(map(lambda x: x[5:], date))

    for i in range(0, len(date)):
        if (i+1) % 2 != 0:
            date[i] = ''

    plt.plot(ind, trading[0])
    plt.xticks(ind, date, rotation='vertical')
    plt.xlabel('日期', fontproperties=prop)
    plt.ylabel('交易量', fontproperties=prop)

    plt.show()
    pass


def draw_index_volatility():
    data_dir = '/Users/rahul/tmp/index_data/'
    shanghai = '000001.csv'
    shenzhen = '399106.csv'
    hs300 = '399300.csv'

    begin_date, end_date = '2015-07-01', '2015-09-30'
    (date, shanghai_close) = read_raw_data(data_dir, file=shanghai, begin_date=begin_date, end_date=end_date, columns=['close'], delimiter=' ')
    (date, shenzhen_close) = read_raw_data(data_dir, file=shenzhen, begin_date=begin_date, end_date=end_date, columns=['close'], delimiter=' ')
    (date, hs300_close) = read_raw_data(data_dir, file=hs300, begin_date=begin_date, end_date=end_date, columns=['close'], delimiter=' ')

    shanghai_vol = read_data('/Users/rahul/tmp/index_data/volatility/', file='000001', begin_date=begin_date, end_date=end_date)
    shenzhen_vol = read_data('/Users/rahul/tmp/index_data/volatility/', file='399106', begin_date=begin_date, end_date=end_date)
    hs300_vol = read_data('/Users/rahul/tmp/index_data/volatility/', file='399300', begin_date=begin_date, end_date=end_date)

    ind = np.arange(len(date))
    # f = '/System/Library/Fonts/STHeiti Medium.ttc'
    f = '/Users/rahul/Library/Fonts/simsun.ttf'
    prop = fm.FontProperties(fname=f)
    date = list(map(lambda x: x[5:], date))
    # for i in range(0, 200):
    #     if (i+1) % 10 != 0:
    #         date[i] = ''

    fig = plt.figure(1)
    fig.suptitle('沪深300指数变化与波动性变化', fontproperties=prop)

    plt.subplot(211)
    plt.plot(ind, hs300_close[0])
    plt.ylabel('指数', fontproperties=prop)
    plt.xticks(ind, date, rotation='vertical')
    # plt.tick_params(axis='x', which='both', bottom='off', top='off', labelbottom='off')
    plt.grid(True)

    plt.subplot(212)
    plt.plot(ind, hs300_vol)
    plt.xticks(ind, date, rotation='vertical')
    plt.ylabel('波动性', fontproperties=prop)
    plt.grid(True)
    # plt.plot(ind, shanghai_close[0], label='上证综指')
    # plt.plot(ind, shenzhen_close[0], label='深证综指')
    # plt.plot(ind, hs300_close[0], label='沪深300')
    # plt.xticks(ind, date, rotation='vertical', fontsize=5)
    # plt.legend(prop=prop, loc='upper right')
    # plt.xlabel('日期', fontproperties=prop)
    # plt.ylabel('指数', fontproperties=prop)
    # plt.grid(True)
    # plt.gcf().autofmt_xdate()

    plt.show()


def draw_degree_distribution():
    x = np.arange(0, 100)
    y = x ** -2.5
    plt.plot(x, y)
    plt.xlabel('k')
    plt.ylabel('p(k)')
    plt.show()


def main():
    # draw_index()
    # draw_trading_volume()
    draw_index_volatility()
    # draw_degree_distribution()


if __name__ == '__main__':
    main()
