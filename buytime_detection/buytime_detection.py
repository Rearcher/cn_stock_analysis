import csv
import logging
import os
from multiprocessing import Pool

from utils import date_util


def detect_one_stock(input_file, filter):
    dates, trade_num, trade_money, buy_time = [], [], [], []
    trade_num_min, trade_num_max = 0, 0

    with open(input_file) as csvfile:
        csv_reader = csv.reader(csvfile)

        for row in csv_reader:
            if csv_reader.line_num == 1:
                continue

            current_date = date_util.to_date(row[0])
            if current_date < date_util.to_date('2015-07-03'):
                continue
            elif current_date > date_util.to_date('2015-10-01'):
                break

            current_trade_num = int(row[5])
            if trade_num_min == 0 and trade_num_max == 0:
                trade_num_max, trade_num_min = current_trade_num, current_trade_num
            else:
                if current_trade_num < trade_num_min:
                    trade_num_min = current_trade_num
                if current_trade_num > trade_num_max:
                    trade_num_max = current_trade_num

            dates.append(row[0])
            trade_num.append(current_trade_num)
            trade_money.append(float(row[6]))

    trade_num_gap, trade_len = trade_num_max - trade_num_min, len(dates)
    for i in range(0, trade_len):
        left_bound, right_bound = i, i
        while left_bound - 1 > 0 and trade_num[left_bound - 1] < trade_num[left_bound]:
            left_bound -= 1
        while right_bound + 1 < trade_len and trade_num[right_bound + 1] < trade_num[right_bound]:
            right_bound += 1
        if (left_bound <= i < right_bound or left_bound < i <= right_bound) \
                and max(trade_num[i] - trade_num[left_bound], trade_num[i] - trade_num[right_bound]) >= trade_num_gap * filter \
                and date_util.to_date(dates[i]) > date_util.to_date('2015-07-03'):
            buy_time.append((dates[i], trade_num[i], trade_money[i]))

    result = input_file[len(input_file)-10:len(input_file)-4]
    for i in range(0, len(buy_time)):
        result += ' ' + buy_time[i][0] + ' ' + str(buy_time[i][1]) + ' ' + str(buy_time[i][2])
    return result


def detect_all_stock(input_dir, filter):
    with open('../resources/national_team_investment.csv') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        valid_stock = [row['股票代码'] for row in csv_reader]
    print(valid_stock)


    pool = Pool(4)
    input_files = os.listdir(input_dir)
    for input_file in input_files:
        if input_file.index('.') == 0:
            print('invalid input file ', input_file)
            continue
        # if input_file[:6] not in valid_stock:
        if not input_file[:6].startswith('60'):
            print('invalid input file ', input_file)
            continue

        if input_file[:6] not in valid_stock:
            print('invalid input file ', input_file)
            continue

        pool.apply_async(detect_one_stock, args=(input_dir + input_file, filter), callback=logging.info)
    pool.close()
    pool.join()


def main():
    # log_util.log_config('../logs/buytime.log')
    logging.basicConfig(level=logging.INFO, format='%(message)s', filename='../logs/buytime_2.log', filemode='w')
    console_log_handler = logging.StreamHandler()
    console_log_handler.setLevel(logging.INFO)
    console_log_handler.setFormatter(logging.Formatter('%(message)s'))
    logging.getLogger().addHandler(console_log_handler)

    data_dir = '/Users/rahul/tmp/data/aligned_data/'
    detect_all_stock(data_dir, filter=0.3)
    # analysis_all(data_dir, filter=0.3, idx=6)
    # res = analysis_single(data_dir + '000001.txt', filter=0.1, idx=6)
    # print(res)
    # print(detect_one_stock(data_dir + '000001.txt', filter=0.3))
    pass


if __name__ == '__main__':
    main()
