"""Align stocks' date.

   1. Use date_ruler as standard date, generated by Shanghai composite index
   2. Input directory: ../data/normalized_data/
   3. Output directory: ../data/aligned_data/

   If one stock doesn't have data on some date in date_ruler, add fake data using previous data.
   When the number of fake data is too big, it means this stock may suspended for a while, excludes
   it or not is up to you.
"""
import os
import logging
from multiprocessing import Pool
from utils.date_util import to_date
from utils.log_util import log_config


def get_date_ruler(begin_date, end_date):
    """
    get date ruler from begin_date to end_date, begin_date and end_date must be valid
    :param begin_date: begin of date ruler
    :param end_date: end of date ruler
    :return: date ruler from begin_date to end_date
    """
    date_input = open('date_ruler', 'r')
    d_format = '%Y-%m-%d'
    begin_date = to_date(begin_date, d_format)
    end_date = to_date(end_date, d_format)

    all_date = date_input.read().split('\n')
    all_date = all_date[:len(all_date) - 1]
    all_date = map(lambda date: to_date(date, d_format), all_date)

    result = []
    for date in all_date:
        if date < begin_date:
            continue
        if date > end_date:
            break
        result.append(date)

    date_input.close()
    return result


def align_single_file(input_filename, output_filename, date_ruler, fake_limit):
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
    if len(output_arr) < ruler_size:
        if ruler_size - len(output_arr) + fake_cnt > fake_limit:
            logging.error(input_filename + " doesn't have enough data")
            return
        else:
            while ruler_idx < ruler_size:
                fake_line = prev_line.split(',')
                fake_line[0] = str(date_ruler[ruler_idx])
                output_arr.append(','.join(fake_line))
                fake_cnt += 1
                ruler_idx += 1

    # write aligned data
    output_file = open(output_filename, 'w')
    output_file.write(''.join(output_arr))
    output_file.close()

    logging.info(input_filename + ': fake cnt = ' + str(fake_cnt))


def align_all_file(input_directory, output_directory):
    date_ruler = get_date_ruler('2015-01-05', '2015-11-02')
    files = os.listdir(input_directory)

    cnt = 1
    for file in files:
        input_filename = input_directory + '/' + file
        output_filename = output_directory + '/' + file
        logging.info('processing ' + str(cnt) + ' ' + input_filename + ' ==> ' + output_filename)
        align_single_file(input_filename, output_filename, date_ruler, 10)
        cnt += 1


def align_all_file_parallel(input_directory, output_directory):
    date_ruler = get_date_ruler('2015-01-05', '2015-11-02')
    files = os.listdir(input_directory)

    cnt = 1
    p = Pool(4)
    for file in files:
        input_filename = input_directory + '/' + file
        output_filename = output_directory + '/' + file
        logging.info('processing ' + str(cnt) + ' ' + input_filename + ' ==> ' + output_filename)
        p.apply(align_single_file, (input_filename, output_filename, date_ruler, 10))
        cnt += 1

    p.close()
    p.join()


def main():
    log_config('../logs/align.log')
    # align_all_file('../data/normalized_data', '../data/aligned_data')
    align_all_file_parallel('../data/normalized_data', '../data/aligned_data')

    # date_ruler = get_date_ruler('2015-01-05', '2015-11-02')
    # align_single_file('../data/normalized_data/000007.txt', 'test', date_ruler, 10)


if __name__ == '__main__':
    main()
