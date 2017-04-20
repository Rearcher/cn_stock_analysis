import collections

from utils.data_util import read_data
from utils.data_util import read_raw_data
import csv


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
    :param date: 
    :return: 
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
                    res[key] += 1
                else:
                    res[key] = 1
    else:
        res = {'in':0, 'out':0}
        for code in stock:
            if code in stocks:
                res['in'] += 1
            else:
                res['out'] += 1
    res = collections.OrderedDict(sorted(res.items(), key=lambda x:x[1], reverse=True))
    return res


def main():
    index_number = '000016'
    date_1 = get_price_raise_date(index_number)
    date_2 = get_vol_decrease_date(index_number)
    date_3 = [val for val in date_1 if val in date_2]

    type = 'hs300s'
    print('date1===')
    for date in date_1:
        print(date, get_classification_list(get_buy_stock_by_date(date), type))

    print('date2===')
    for date in date_2:
        print(date, get_classification_list(get_buy_stock_by_date(date), type))

    print('date3===')
    for date in date_3:
        print(date, get_classification_list(get_buy_stock_by_date(date), type))


if __name__ == '__main__':
    main()
    # get_classification_list([], 'industry')