import csv
import logging
import os
from multiprocessing import Pool

from utils import date_util
from utils import log_util


def analysis_single(input_file, filter):
    dates, trades, buytime = [], [], []
    trade_min, trade_max = 0, 0

    # acquire date and trade volumes
    with open(input_file) as csvfile:
        csv_reader = csv.reader(csvfile)

        for row in csv_reader:
            # skip column name
            if csv_reader.line_num == 1:
                continue

            current_date = date_util.to_date(row[0], '%Y-%m-%d')
            if current_date < date_util.to_date('2015-07-01', '%Y-%m-%d'):
                continue

            # handle trade max & trade min
            current_trade = int(row[5])
            if trade_min == 0 and trade_max == 0:
                trade_min, trade_max = current_trade, current_trade
            else:
                if current_trade < trade_min:
                    trade_min = current_trade
                if current_trade > trade_max:
                    trade_max = current_trade

            dates.append(row[0])
            trades.append(current_trade)

    trade_gap, trade_len, trade_sum = trade_max - trade_min, len(trades), 0
    for i in range(0, trade_len):
        left_bound, right_bound = i, i

        while left_bound - 1 > 0 and trades[left_bound - 1] < trades[left_bound]:
            left_bound -= 1
        while right_bound + 1 < trade_len and trades[right_bound + 1] < trades[right_bound]:
            right_bound += 1

        if left_bound < i and right_bound > i \
                and max(trades[i] - trades[left_bound], trades[i] - trades[right_bound]) >= trade_gap * filter \
                and date_util.to_date(dates[i], '%Y-%m-%d') > date_util.to_date('2015-07-01', '%Y-%m-%d'):
            buytime.append(dates[i])
            trade_sum += trades[i]

    result = input_file + ' ' + str(len(buytime))
    for time in buytime:
        result += ' ' + time
    return result


def analysis_all(input_dir, filter):
    pool = Pool(4)
    input_files = os.listdir(input_dir)
    for input_file in input_files:
        if input_file.index('.') == 0:
            print('invalid input file', input_file)
            continue
        pool.apply_async(analysis_single, args=(input_dir + input_file, filter), callback=logging.info)
    pool.close()
    pool.join()


def main():
    log_util.log_config('../logs/buytime.log')
    data_dir = '/Users/rahul/tmp/data/aligned_data/'
    analysis_all(data_dir, 0.3)
    # analysis_single(data_dir + '000001.txt', filter=0.1)
    pass


if __name__ == '__main__':
    main()
