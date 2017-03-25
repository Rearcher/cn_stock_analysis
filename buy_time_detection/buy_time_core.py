import collections
import os

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np

from utils.data_util import get_valid_stock
from utils.data_util import read_raw_data
from utils.data_util import read_data


def get_buy_time(date_ruler, ts, percent=0.1):
    """
    根据某只股票的交易量确定国家队买入的日期
    :param date_ruler: 日期
    :param ts: 交易量
    :param percent: 按峰高的百分比过滤
    :return: 买入日期
    """

    assert len(date_ruler) == len(ts)

    ts_max, ts_min, buy_time = max(ts), min(ts), []
    threshold = (ts_max - ts_min) * percent

    for i in range(0, len(ts)):

        left_bound, right_bound = i, i

        while left_bound - 1 > 0 and ts[left_bound - 1] < ts[left_bound]:
            left_bound -= 1

        while right_bound + 1 < len(ts) and ts[right_bound + 1] < ts[right_bound]:
            right_bound += 1

        current_gap = max(ts[i] - ts[left_bound], ts[i] - ts[right_bound])
        if (left_bound < i < right_bound or left_bound < i < right_bound) and current_gap >= threshold:
            if date_ruler[i] < '2015-07-06':
                continue
            buy_time.append((i, date_ruler[i]))

    return buy_time


def get_buy_summary():
    """
    获取每个买入日期的买入的股票数和这些股票当天的交易额总量
    :return: 日期、每天的股票买入数、每天的股票交易总额
    """
    data_dir = '/Users/rahul/tmp/data/aligned_data/'
    files = os.listdir(data_dir)

    begin_date, end_date = '2015-07-01', '2015-09-30'
    stock_number_summary, stock_money_summary = {}, {}

    # 保存每个买入日期买入的股票
    stock_to_time_map, time_to_stock_map = {}, {}
    valid_stock = get_valid_stock()

    for file in files:
        if file.startswith('.'):
            continue
        if file[:6] not in valid_stock:
            continue
        if file.startswith('300') or file.startswith('002'):
            continue
        date_ruler, returns = read_raw_data(data_dir=data_dir, file=file, begin_date=begin_date, end_date=end_date,
                                            columns=['close', 'trading_volume', 'transaction_volume'])
        close, trading_volume, transaction_volume = returns[0], returns[1], returns[2]
        buytime = get_buy_time(date_ruler, trading_volume)

        stock_to_time_map[file[:6]] = []
        for (idx, time) in buytime:
            stock_to_time_map[file[:6]].append(time)

            if time in stock_number_summary.keys():
                stock_number_summary[time].append(file[:6])
                stock_money_summary[time] += transaction_volume[idx]
            else:
                stock_number_summary[time] = [file[:6]]
                stock_money_summary[time] = transaction_volume[idx]

            if time in time_to_stock_map.keys():
                time_to_stock_map[time].append(file[:6])
            else:
                time_to_stock_map[time] = [file[:6]]

    stock_number_summary = collections.OrderedDict(sorted(stock_number_summary.items()))
    stock_money_summary = collections.OrderedDict(sorted(stock_money_summary.items()))

    x, y1, y2 = [], [], []
    for k, v in stock_number_summary.items():
        x.append(k)
        y1.append(len(v))

    for k, v in stock_money_summary.items():
        y2.append(v)

    with open('../resources/stock_to_time', 'w') as f:
        for k, v in stock_to_time_map.items():
            f.write(k + ' ' + ' '.join(v) + '\n')

    with open('../resources/time_to_stock', 'w') as f:
        for k, v in time_to_stock_map.items():
            f.write(k + ' ' + ' '.join(v) + '\n')

    return x, y1, y2


def get_price_change_by_time(lag=0):
    """
    根据买入日期来判断买入使得股价上升还是升高
    :param lag: lag为0时，判断买入当天的股价和买入前一天的股价，lag为1时，判断买入后一天的股价与买入前一天的股价，以此类推
    :return: 每个买入日期买入行为造成lag天后股价上涨的股票数、百分比
    """
    data_dir = '/Users/rahul/tmp/data/aligned_data/'
    files = os.listdir(data_dir)

    begin_date, end_date = '2015-07-01', '2015-09-30'
    valid_stock = get_valid_stock()

    price_summary = {}

    for file in files:
        if file.startswith('.'):
            continue
        if file[:6] not in valid_stock:
            continue
        if file.startswith('002') or file.startswith('300'):
            continue

        date_ruler, returns = read_raw_data(data_dir=data_dir, file=file, begin_date=begin_date, end_date=end_date,
                                            columns=['close', 'trading_volume', 'transaction_volume'])
        close, trading_volume, transaction_volume = returns[0], returns[1], returns[2]
        buytime = get_buy_time(date_ruler, trading_volume)

        for (idx, time) in buytime:
            if time not in price_summary.keys():
                price_summary[time] = [0, 0]

            if idx > 0 and idx + lag < len(close) and close[idx+lag] >= close[idx-1]:
                price_summary[time][0] += 1
            else:
                price_summary[time][1] += 1

    price_summary = collections.OrderedDict(sorted(price_summary.items()))
    x, y = [], []

    for k, v in price_summary.items():
        x.append(v[0])
        y.append(v[0] / (v[0]+v[1]))

    return x, y


def get_price_change_by_stock():
    data_dir = '/Users/rahul/tmp/data/aligned_data/'
    files = os.listdir(data_dir)

    begin_date, end_date = '2015-07-01', '2015-09-30'
    valid_stock = get_valid_stock()

    stock_summary = {}

    for file in files:
        if file.startswith('.'):
            continue
        if file[:6] not in valid_stock:
            continue
        if file.startswith('002') or file.startswith('300'):
            continue

        date_ruler, returns = read_raw_data(data_dir=data_dir, file=file, begin_date=begin_date, end_date=end_date,
                                            columns=['close', 'trading_volume', 'transaction_volume'])
        close, trading_volume, transaction_volume = returns[0], returns[1], returns[2]
        buytime = get_buy_time(date_ruler, trading_volume)

        for (idx, time) in buytime:
            if file[:6] not in stock_summary.keys():
                stock_summary[file[:6]] = [0, 0]

            if idx > 0 and close[idx] > close[idx - 1]:
                stock_summary[file[:6]][0] += 1
            else:
                stock_summary[file[:6]][1] += 1

    stocks, price_raise_percent = [], []
    with open('../resources/price_raise_percent', 'w') as f:
        for k, v in stock_summary.items():
            stocks.append(k)
            price_raise_percent.append(v[0] / sum(v))
            f.write(k + ' ' + str(v[0] / sum(v)) + '\n')

    return stocks, price_raise_percent


def get_volatility_change_by_time(lag=0):
    """
    根据买入日期来判断买入使得股票波动性是上升还是升高
    :param lag: lag为0时，判断买入当天的股价和买入前一天的股价，lag为1时，判断买入后一天的股价与买入前一天的股价，以此类推
    :return: 每个买入日期买入行为造成lag天后股票波动性上涨的股票数、百分比
    """
    data_dir = '/Users/rahul/tmp/data/aligned_data/'
    volatility_dir = '/Users/rahul/tmp/volatility/'
    files = os.listdir(data_dir)
    volatility_files = os.listdir(volatility_dir)

    begin_date, end_date = '2015-07-01', '2015-09-30'
    valid_stock = get_valid_stock()

    price_summary = {}

    for file in files:
        if file.startswith('.'):
            continue
        if file[:6] not in valid_stock:
            continue
        if file.startswith('002') or file.startswith('300'):
            continue

        volatility_file = 'sig_' + file[:6]
        if volatility_file not in volatility_files:
            continue

        date_ruler, returns = read_raw_data(data_dir=data_dir, file=file, begin_date=begin_date, end_date=end_date,
                                            columns=['close', 'trading_volume', 'transaction_volume'])
        close, trading_volume, transaction_volume = returns[0], returns[1], returns[2]
        buytime = get_buy_time(date_ruler, trading_volume)
        volatility = read_data(data_dir=volatility_dir, file=volatility_file, begin_date=begin_date, end_date=end_date)

        for (idx, time) in buytime:
            if time not in price_summary.keys():
                price_summary[time] = [0, 0]

            if idx > 0 and idx + lag < len(volatility) and volatility[idx+lag] > volatility[idx-1]:
                price_summary[time][1] += 1
            else:
                price_summary[time][0] += 1

    price_summary = collections.OrderedDict(sorted(price_summary.items()))
    x, y = [], []

    for k, v in price_summary.items():
        x.append(v[0])
        y.append(v[0] / (v[0]+v[1]))

    return x, y


def get_volatility_change_by_stock():
    data_dir = '/Users/rahul/tmp/data/aligned_data/'
    volatility_dir = '/Users/rahul/tmp/volatility/'

    files = os.listdir(data_dir)
    volatility_files = os.listdir(volatility_dir)

    begin_date, end_date = '2015-07-01', '2015-09-30'
    valid_stock = get_valid_stock()

    stock_summary = {}

    for file in files:
        if file.startswith('.'):
            continue
        if file[:6] not in valid_stock:
            continue
        if file.startswith('002') or file.startswith('300'):
            continue

        volatility_file = 'sig_' + file[:6]
        if volatility_file not in volatility_files:
            continue

        date_ruler, returns = read_raw_data(data_dir=data_dir, file=file, begin_date=begin_date, end_date=end_date,
                                            columns=['close', 'trading_volume', 'transaction_volume'])
        close, trading_volume, transaction_volume = returns[0], returns[1], returns[2]
        buytime = get_buy_time(date_ruler, trading_volume)
        volatility = read_data(data_dir=volatility_dir, file=volatility_file, begin_date=begin_date, end_date=end_date)

        for (idx, time) in buytime:
            if file[:6] not in stock_summary.keys():
                stock_summary[file[:6]] = [0, 0]

            if idx > 0 and volatility[idx] <= volatility[idx - 1]:
                stock_summary[file[:6]][0] += 1
            else:
                stock_summary[file[:6]][1] += 1

    stocks, volatility_drop_percent = [], []
    with open('../resources/volatility_drop_percent', 'w') as f:
        for k, v in stock_summary.items():
            stocks.append(k)
            volatility_drop_percent.append(v[0] / sum(v))
            f.write(k + ' ' + str(v[0] / sum(v)) + '\n')

    return stocks, volatility_drop_percent


def after_buy_time_analysis():
    data_dir = '/Users/rahul/tmp/data/aligned_data/'
    volatility_dir = '/Users/rahul/tmp/volatility/'

    data_files = os.listdir(data_dir)
    volatility_files = os.listdir(volatility_dir)

    begin_date, end_date = '2015-07-01', '2015-09-30'
    valid_stock = get_valid_stock()

    price_result, volatility_result = {}, {}

    for file in data_files:
        if file.startswith('.'):
            continue
        if file[:6] not in valid_stock:
            continue
        if file.startswith('002') or file.startswith('300'):
            continue

        volatility_file = 'sig_' + file[:6]
        if volatility_file not in volatility_files:
            continue

        date_ruler, returns = read_raw_data(data_dir=data_dir, file=file, begin_date=begin_date, end_date=end_date,
                                            columns=['close', 'trading_volume', 'transaction_volume'])
        close, trading_volume, transaction_volume = returns[0], returns[1], returns[2]
        buy_time = get_buy_time(date_ruler, trading_volume)
        volatility = read_data(data_dir=volatility_dir, file=volatility_file, begin_date=begin_date, end_date=end_date)

        buy_time_idx = [idx for (idx, time) in buy_time]
        price_result[file[:6]], volatility_result[file[:6]] = [0, 0], [0, 0]

        i = 0
        while i < len(date_ruler):
            if i not in buy_time_idx:
                i += 1
                continue
            while i + 1 in buy_time_idx and i + 1 < len(date_ruler):
                i += 1
            if i + 1 >= len(date_ruler):
                break

            if close[i + 1] < close[i]:
                # 没有资金注入时，股价下跌
                price_result[file[:6]][0] += 1
            else:
                # 没有资金注入时，股价上升
                price_result[file[:6]][1] += 1

            if volatility[i + 1] > volatility[i]:
                # 没有资金注入时，股票波动性上升
                volatility_result[file[:6]][0] += 1
            else:
                # 没有资金注入时，股票波动性下降
                volatility_result[file[:6]][1] += 1
            i += 1

    with open('../resources/price_drop_percent_after', 'w') as f:
        for k, v in price_result.items():
            f.write(k + ' ' + str(v[0] / (v[0] + v[1])) + '\n')

    with open('../resources/volatility_raise_percent_after', 'w') as f:
        for k, v in volatility_result.items():
            f.write(k + ' ' + str(v[0] / (v[0] + v[1])) + '\n')

    pass


def show():
    """
    展示环节
    :return: null
    """
    x, y1, y2 = get_buy_summary()
    y3, y4 = get_price_change_by_time(lag=0)
    y5, y6 = get_volatility_change_by_time(lag=0)

    ind = np.arange(len(x))
    f = '/System/Library/Fonts/STHeiti Medium.ttc'
    prop = fm.FontProperties(fname=f)
    x = list(map(lambda x: x[5:], x))

    fig = plt.figure(1)
    fig.suptitle('买入时间分析', fontsize=14, fontweight='bold', fontproperties=prop)

    plt.subplot(111)
    plt.plot(ind, y1, label='买入当天买入的股票数')
    plt.plot(ind, y3, color='red', label='买入当天买入的股票中股价上升的股票数')
    plt.plot(ind, y5, color='green', label='买入当天买入的股票中波动性下降的股票数')
    plt.xticks(ind, x, rotation='vertical')
    plt.ylabel('股票数', fontproperties=prop)
    plt.grid(True)
    plt.legend(prop=prop, loc='upper right')

    # plt.subplot(212)
    # plt.plot(ind, y2)
    # plt.xticks(ind, x, rotation='vertical')
    # plt.ylabel('买入金额', fontproperties=prop)
    # plt.grid(True)

    print(np.corrcoef(y1, y3))
    print(np.corrcoef(y1, y5))
    print(np.corrcoef(y3, y5))
    plt.show()


def main():
    # date, buy_number, buy_money = get_buy_summary()
    # print(np.corrcoef(buy_number, buy_money))
    #
    # x, price_change = get_price_change_by_time(lag=0)
    # print(np.corrcoef([buy_number, buy_money], [x, price_change]))
    # show()
    # get_price_change_by_stock()
    # get_volatility_change_by_stock()
    # get_buy_summary()
    after_buy_time_analysis()
    pass


if __name__ == '__main__':
    main()
