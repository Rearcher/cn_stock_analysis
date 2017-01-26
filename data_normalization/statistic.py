import os
import logging
from multiprocessing import Pool
from utils.date_util import to_date
from utils.date_util import get_date_ruler
from utils.log_util import log_config

def fake_day_cnt(input_filename, date_ruler, fake_limit):
    input_file = open(input_filename, 'r')
    output_arr = []

    # process header
    line = input_file.readline()
    output_arr.append(line)

    # date_ruler index to point out current date
    ruler_idx = 0

    # date_ruler size
    ruler_size = len(date_ruler)

    # fake data count
    fake_cnt = 0

    line = input_file.readline()
    prev_line = line
    prev_date = to_date(line.split(',')[0], '%Y-%m-%d')
    while line:

        line_arr = line.split(',')
        cur_date = to_date(line_arr[0], '%Y-%m-%d')

        if cur_date < prev_date:
            input_file.close()
            logging.error('input file ' + input_filename + ' is invalid!')
            return

        # skip data before begin date
        if cur_date < date_ruler[0]:
            prev_line = line
            prev_date = cur_date
            line = input_file.readline()
            continue

        # skip data after end date
        if cur_date > date_ruler[ruler_size - 1]:
            break

        # exist real data
        if cur_date == date_ruler[ruler_idx]:
            output_arr.append(line)
        # miss real data
        elif cur_date > date_ruler[ruler_idx]:
            while date_ruler[ruler_idx] < cur_date:
                fake_line = prev_line.split(',')
                fake_line[0] = str(date_ruler[ruler_idx])
                output_arr.append(','.join(fake_line))
                fake_cnt += 1
                ruler_idx += 1
            # exceed fake limit, abandon this stock
            if fake_cnt > fake_limit:
                input_file.close()
                logging.info(input_filename + ' exceeds fake limit ' + str(fake_limit))
                return

            output_arr.append(line)

        # meet date ruler end
        if cur_date == date_ruler[ruler_size - 1]:
            break

        prev_line = line
        prev_date = cur_date
        ruler_idx += 1
        line = input_file.readline()

    input_file.close()

    # verify enough data
    if len(output_arr) <= ruler_size:
        if ruler_size - len(output_arr) + 1 + fake_cnt > fake_limit:
            logging.error(input_filename + " doesn't have enough data")
            return
        else:
            while ruler_idx < ruler_size:
                fake_line = prev_line.split(',')
                fake_line[0] = str(date_ruler[ruler_idx])
                output_arr.append(','.join(fake_line))
                fake_cnt += 1
                ruler_idx += 1

    logging.info(input_filename + ' ' + str(fake_cnt))


def main():
    log_config('../logs/statistic.log')

    date_ruler = get_date_ruler('2015-06-01', '2015-11-02')
    input_directory = '../data/normalized_data'
    files = os.listdir(input_directory)

    p = Pool(4)

    for file in files:
        input_filename = input_directory + '/' + file
        p.apply(fake_day_cnt, args=(input_filename, date_ruler, 1000))


if __name__ == '__main__':
    main()