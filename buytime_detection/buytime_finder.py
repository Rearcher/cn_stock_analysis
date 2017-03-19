import collections
import csv
import os

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np


def simple_line_plot(date_ruler, ts):
    ind = np.arange(len(date_ruler))
    f = '/System/Library/Fonts/STHeiti Medium.ttc'
    prop = fm.FontProperties(fname=f)

    plt.plot(ind, ts)
    plt.xticks(ind, date_ruler, rotation='vertical')
    plt.grid(True)
    plt.show()


def get_valid_stock():
    with open('../resources/national_team_investment.csv') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        valid_stock = [row['股票代码'] for row in csv_reader]
    return valid_stock


def get_ts(filename, begin_date, end_date):
    with open(filename, 'r') as f:
        csv_reader = csv.DictReader(f)
        trading_volume = [float(row['trading_volume']) for row in csv_reader]

        f.seek(0)
        csv_reader = csv.DictReader(f)
        transaction_volume = [float(row['transaction_volume']) for row in csv_reader]

        f.seek(0)
        csv_reader = csv.DictReader(f)
        close = [float(row['close']) for row in csv_reader]

        f.seek(0)
        csv_reader = csv.DictReader(f)
        date_ruler = [row['date'] for row in csv_reader]

        begin_idx = date_ruler.index(begin_date)
        end_idx = date_ruler.index(end_date)

        trading_volume = trading_volume[begin_idx:end_idx + 1]
        transaction_volume = transaction_volume[begin_idx:end_idx + 1]
        date_ruler = date_ruler[begin_idx:end_idx + 1]

    return date_ruler, trading_volume, transaction_volume, close


def buytime_finder(date_ruler, ts, percent=0.1):
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


def plot_trades(stock_num, begin_date, end_date):
    data_dir = '/Users/rahul/tmp/data/aligned_data/'
    filename = data_dir + stock_num + '.txt'

    date_ruler, ts, tt, to= get_ts(filename, begin_date, end_date)
    print(buytime_finder(date_ruler, ts))
    simple_line_plot(date_ruler, ts)


def buytime_summary():
    data_dir = '/Users/rahul/tmp/data/aligned_data/'
    files = os.listdir(data_dir)

    begin_date, end_date = '2015-07-01', '2015-09-30'
    stock_number_summary, stock_money_summary = {}, {}
    valid_stock = get_valid_stock()

    for file in files:
        if file.startswith('.'):
            continue
        if file[:6] not in valid_stock:
            continue
        if file.startswith('300') or file.startswith('002'):
            continue
        filename = data_dir + file
        date_ruler, trading_volume, transaction_volume, close = get_ts(filename, begin_date, end_date)
        buytime = buytime_finder(date_ruler, trading_volume)

        for (idx, time) in buytime:
            if time in stock_number_summary.keys():
                stock_number_summary[time].append(file[:6])
                stock_money_summary[time] += transaction_volume[idx]
            else:
                stock_number_summary[time] = [file[:6]]
                stock_money_summary[time] = transaction_volume[idx]

    stock_number_summary = collections.OrderedDict(sorted(stock_number_summary.items()))
    stock_money_summary = collections.OrderedDict(sorted(stock_money_summary.items()))

    x, y1, y2 = [], [], []
    for k, v in stock_number_summary.items():
        x.append(k)
        y1.append(len(v))

    for k, v in stock_money_summary.items():
        y2.append(v)

    ind = np.arange(len(x))
    f = '/System/Library/Fonts/STHeiti Medium.ttc'
    prop = fm.FontProperties(fname=f)
    x = list(map(lambda x: x[5:], x))

    fig = plt.figure(1)
    fig.suptitle('买入时间统计', fontsize=14, fontweight='bold', fontproperties=prop)

    plt.subplot(311)
    plt.plot(ind, y1)
    plt.xticks(ind, x, rotation='vertical')
    plt.ylabel('买入股票数', fontproperties=prop)
    plt.grid(True)

    plt.subplot(312)
    plt.plot(ind, y2, color='red')
    plt.xticks(ind, x, rotation='vertical')
    plt.ylabel('买入金额', fontproperties=prop)
    plt.grid(True)

    plt.subplot(313)
    plt.plot(ind, buytime_with_price(), color='green')
    plt.xticks(ind, x, rotation='vertical')
    plt.ylabel('买入当天股价上升的股票数百分比', fontproperties=prop)
    plt.grid(True)

    plt.show()


def buytime_with_price():
    data_dir = '/Users/rahul/tmp/data/aligned_data/'
    files = os.listdir(data_dir)

    begin_date, end_date = '2015-07-01', '2015-09-30'
    valid_stock = get_valid_stock()

    price_summary = {}
    stock_summary = {}

    for file in files:
        if file.startswith('.'):
            continue
        if file[:6] not in valid_stock:
            continue
        if file.startswith('002') or file.startswith('300'):
            continue

        filename = data_dir + file
        date_ruler, trading_volume, transaction_volume, close = get_ts(filename, begin_date, end_date)
        buytime = buytime_finder(date_ruler, trading_volume)

        for (idx, time) in buytime:
            if time not in price_summary.keys():
                price_summary[time] = [0, 0]
            if file[:6] not in stock_summary.keys():
                stock_summary[file[:6]] = [0, 0]

            if idx > 0 and close[idx] > close[idx-1]:
            # if idx + 1 < len(close) and close[idx] < close[idx + 1]:
                price_summary[time][0] += 1
                stock_summary[file[:6]][0] += 1
            else:
                price_summary[time][1] += 1
                stock_summary[file[:6]][1] += 1

    price_summary = collections.OrderedDict(sorted(price_summary.items()))
    x, y = [], []

    for k, v in price_summary.items():
        x.append(k)
        y.append(v[0] / (v[0]+v[1]))

    # ind = np.arange(len(x))
    # f = '/System/Library/Fonts/STHeiti Medium.ttc'
    # prop = fm.FontProperties(fname=f)
    # x = list(map(lambda x: x[5:], x))
    #
    # plt.plot(ind, y)
    # plt.title('国家队买入对股价的影响', fontproperties=prop)
    # plt.xticks(ind, x, rotation='vertical')
    # plt.ylabel('买入当天股价上升的股票数百分比', fontproperties=prop)
    # plt.grid(True)
    # plt.show()

    with open('stock_summary', 'w') as f:
        for k, v in stock_summary.items():
            line = k + ' ' + str(v[0] / (v[0] + v[1]))
            f.write(line + '\n')

    return y
    pass


def buytime_with_volatility():
    pass


def main():
    # plot_trades('601288', '2015-07-01', '2015-09-30')
    # plot_trades('000501', '2015-07-01', '2015-11-02')
    buytime_summary()
    pass

if __name__ == '__main__':
    main()
