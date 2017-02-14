import csv
import logging
import os
from multiprocessing import Pool

from utils import date_util


def analysis_single(input_file, filter, idx):
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
            elif current_date > date_util.to_date('2015-10-01', '%Y-%m-%d'):
                break

            # handle trade max & trade min
            if idx == 5:
                current_trade = int(row[5])
            else:
                current_trade = float(row[6])
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

        if left_bound < i < right_bound \
                and max(trades[i] - trades[left_bound], trades[i] - trades[right_bound]) >= trade_gap * filter \
                and date_util.to_date(dates[i], '%Y-%m-%d') > date_util.to_date('2015-07-01', '%Y-%m-%d'):
            buytime.append(dates[i])
            trade_sum += trades[i]

    # result = input_file + ' ' + str(len(buytime))
    result = input_file[len(input_file)-10:len(input_file)-4]
    for time in buytime:
        result += ' ' + time
    return result


def analysis_all(input_dir, filter, idx):
    pool = Pool(4)
    input_files = os.listdir(input_dir)
    for input_file in input_files:
        if input_file.index('.') == 0:
            print('invalid input file', input_file)
            continue
        pool.apply_async(analysis_single, args=(input_dir + input_file, filter, idx), callback=logging.info)
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
    analysis_all(data_dir, filter=0.3, idx=6)
    # res = analysis_single(data_dir + '000001.txt', filter=0.1, idx=6)
    # print(res)
    pass


if __name__ == '__main__':
    main()
