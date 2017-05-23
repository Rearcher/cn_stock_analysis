import collections
import csv

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

from utils.data_util import read_data
from utils.data_util import read_raw_data


def get_index_data(index_number):
    """
    获取某一项综合指数的数据，返回日期、收盘价、波动性
    :param index_number: 
    :return: 
    """
    data_dir = '/Users/rahul/tmp/index_data/'
    volatility_dir = data_dir + 'volatility/'
    begin_date, end_date = '2015-07-01', '2015-09-30'

    date, close = read_raw_data(data_dir, index_number + '.csv', begin_date=begin_date, end_date=end_date,
                                columns=['close'], delimiter=' ')
    volatility = read_data(volatility_dir, index_number, begin_date=begin_date, end_date=end_date)

    return date, close[0], volatility


def get_price_raise_date(index_number):
    """
    获取某一项综合指数相比于前一天上升的日期
    :param index_number: 
    :return: 
    """
    date, close, _ = get_index_data(index_number)
    result = []
    for i in range(0, len(date)):
        if i == 0:
            continue
        if close[i] > close[i-1]:
            result.append(date[i])
    return result


def get_vol_decrease_date(index_number):
    """
    获取某一项综合指数的波动性相比于前一天下降的日期
    :param index_number: 
    :return: 
    """
    date, _, vol = get_index_data(index_number)
    result = []
    for i in range(0, len(date)):
        if i == 0:
            continue
        if vol[i] > vol[i-1]:
            result.append(date[i])
    return result


def get_buy_stock_by_date(date):
    """
    根据日期获取当天买入的股票列表，日期格式为YYYY-MM-dd
    :param date: 
    :return: 
    """
    file, res = '../resources/time_to_stock', []
    with open(file, 'r') as f:
        data = f.readlines()

    for line in data:
        cur_date = line[:10]
        if cur_date == date:
            res = line[11:].strip('\n').split(' ')
        if cur_date > date:
            break
    return res


def get_classification_list(stock, classification_type):
    """
    根据股票列表，以及对应的股票分类依据，确定该股票列表中有哪些分类
    classification_type可以是industry/area/concept/hs300s
    :param stock: 
    :param classification_type:
    :return: 一个map(股票分类 --> 对应的股票列表)
    """
    classification_file = '/Users/rahul/tmp/classification/' + classification_type + '.csv'

    with open(classification_file, 'r') as f:
        csv_reader = csv.DictReader(f)
        stocks = [row['code'] for row in csv_reader]

        if classification_type != 'hs300s':
            f.seek(0)
            csv_reader = csv.DictReader(f)
            types = [row['type'] for row in csv_reader]

    res = {}
    if classification_type != 'hs300s':
        for code in stock:
            if code in stocks:
                key = types[stocks.index(code)]
                if key in res.keys():
                    res[key].append(code)
                else:
                    res[key] = [code]
    else:
        res = {'in': [], 'out': []}
        for code in stock:
            if code in stocks:
                res['in'].append(code)
            else:
                res['out'].append(code)
    res = collections.OrderedDict(sorted(res.items(), key=lambda x: len(x[1]), reverse=True))
    return res


def get_driven_stock(stock):
    """
    根据某个股票列表，输出由该列表包含的股票带动的股票列表
    :param stock: 
    :return: 
    """
    pass


def draw_pie(result):
    labels, values = [], []
    for k, v in result.items():
        if (len(labels) < 12):
            labels.append(k)
            values.append(len(v))
        elif (len(labels) == 12):
            labels.append('其他')
            values.append(len(v))
        else:
            values[len(values) - 1] += len(v)

    # f = '/System/Library/Fonts/STHeiti Medium.ttc'
    f = '/Users/rahul/Library/Fonts/simsun.ttf'
    prop = fm.FontProperties(fname=f, size=20)

    fig1, ax1 = plt.subplots()
    pie = plt.pie(values, labels=labels, startangle=90, autopct='%1.1f%%')
    # pie = ax1.pie(values, labels=labels, autopct='%1.1f%%',
    #         shadow=False, startangle=90)
    for font in pie[1]:
        font.set_fontproperties(prop)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.show()


def main():
    index_number = '399300'
    date_1 = get_price_raise_date(index_number)
    date_2 = get_vol_decrease_date(index_number)
    date_3 = [val for val in date_1 if val in date_2]

    print(date_3)
    type = 'area'
    result = {}
    for date in date_3:
        current_map = get_classification_list(get_buy_stock_by_date(date), type)
        for k, v in current_map.items():
            if k in result.keys():
                for code in v:
                    result[k].append(code)
            else:
                result[k] = v

    result = collections.OrderedDict(sorted(result.items(), key=lambda x: len(x[1]), reverse=True))
    draw_pie(result)


if __name__ == '__main__':
    main()
    # get_classification_list([], 'industry')