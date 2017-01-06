"""Calculate each day's return

   return = today.close - yesterday.close

   Input directory: ../data/aligned_data
   Output directory: ../data/returned_data
"""
import os
import logging
from multiprocessing import Pool
from utils.log_util import log_config
from utils.date_util import get_date_ruler


def calc_single_file(input_filename, output_filename):
    f_input = open(input_filename, 'r')
    f_output = open(output_filename, 'w')

    # write new header
    line = f_input.readline()
    line = line[:len(line)-1].split(',')
    line.append('return\n')
    f_output.write(','.join(line))

    line = f_input.readline()
    base_close = float(line.split(',')[4])
    while line:
        cur_close = float(line.split(',')[4])
        cur_return = cur_close - base_close
        f_output.write(line[:len(line)-1] + ',' + str(cur_return) + '\n')

        base_close = cur_close
        line = f_input.readline()

    f_input.close()
    f_output.close()


def calc_all_file(input_directory, output_directory):
    files = os.listdir(input_directory)
    p = Pool(4)

    cnt = 1
    for file in files:
        input_filename = input_directory + '/' + file
        output_filename = output_directory + '/' + file
        logging.info('process ' + str(cnt) + ' : ' + input_filename + ' ==> ' + output_filename)
        p.apply(calc_single_file, args=(input_filename, output_filename))
        cnt += 1

    p.close()
    p.join()


def merge_all(input_directory, column_idx, output_filename):
    """
    merge all data files in input_directory with specified column, eg: merge all returns,
    first column will always be date.
    :param input_directory: data input directory
    :param column_idx: which column to merge, start from 0
    :return: None
    """
    files = os.listdir(input_directory)
    output_arr = get_date_ruler('2015-01-05', '2015-11-02')
    output_arr.insert(0, 'date')
    output_arr = list(map(str, output_arr))

    for file in files:
        idx = 0
        f_input = open(input_directory + '/' + file, 'r')

        output_arr[idx] += ','
        output_arr[idx] += file.split('.')[0]
        idx += 1

        line = f_input.readline()
        line = f_input.readline()
        while line:
            output_arr[idx] += ','
            output_arr[idx] += str(round(float(line.split(',')[column_idx]), 2))
            line = f_input.readline()
            idx += 1

        f_input.close()

    f_output = open(output_filename, 'w')
    f_output.write('\n'.join(output_arr))
    f_output.close()


def main():
    log_config('../logs/return.log')
    # calc_all_file('../data/aligned_data', '../data/returned_data')
    merge_all('../data/returned_data', 7, '../data/return_all.txt')
    merge_all('../data/returned_data', 4, '../data/close_all.txt')

if __name__ == '__main__':
    main()
