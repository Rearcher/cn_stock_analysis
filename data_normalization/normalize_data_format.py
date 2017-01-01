"""Normalize data format.

   Input raw data is in ../A_history_data directory
   Output directory is ../normalized_data

   Normalization operations are:
   1. change file name form SZxxxxxx.txt to xxxxxx.txt
   2. remove first useless information line
   3. change Chinese header to English
   4. remove last useless information line
   5. change date format to %Y-%m-%d
"""
import os
from utils.date_util import to_date


def normalize_single_file(input_filename, output_filename):
    input = open(input_filename, 'r')
    output = open(output_filename, 'w')

    # skip first useless line
    input.readline()

    # skip original header
    input.readline()

    # write new header
    output.write(','.join(['date', 'open', 'high', 'low', 'close', 'trading_volume', 'transaction_volume\n']))

    # real data begins
    line = input.readline()
    while line:
        line = line.split('\t')

        # skip last useless line
        if len(line) <= 2:
            break

        # change date format
        line[0] = str(to_date(line[0], '%Y/%m/%d'))
        output.write(','.join(line))

        line = input.readline()

    input.close()
    output.close()


def normalize_all_file(input_directory, output_directory):
    files = os.listdir(input_directory)

    cnt = 1
    for file in files:
        input_filename = input_directory + '/' + file
        output_filename = output_directory + '/' + file[2:]
        print('processing', cnt, input_filename, '==>', output_filename)
        normalize_single_file(input_filename, output_filename)
        cnt += 1


def main():
    normalize_all_file('../data/A_history_data', '../data/normalized_data')


if __name__ == '__main__':
    main()

