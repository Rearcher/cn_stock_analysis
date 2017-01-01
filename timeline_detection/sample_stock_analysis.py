"""Analysis some stock saved by 'national team'

   1. Extract data from 2015.6.1 to 2015.9.25
   2. Focus on 'close', 'trading_volume', 'transaction_volume'
   3. Input directory: ../data/normalized_data/
   4. Output directory: ../data/timeline_data/
"""
import datetime
from utils.date_util import to_date


def sample_single_file(input_filename, output_filename):
    """
    Extract data from 2015.6.1 to 2015.9.25
    :param input_filename: input filename
    :param output_filename: output filename
    :return: None
    """

    input = open(input_filename, 'r')
    output = open(output_filename, 'w')

    begin_date = datetime.date(2015, 6, 1)
    end_date = datetime.date(2015, 9, 25)

    # write header
    line = input.readline()
    output.write(line)

    # data begins
    line = input.readline()
    while line:
        line = line.split(',')
        cur_date = to_date(line[0], '%Y-%m-%d')

        # filter previous and afterwards data
        if cur_date < begin_date or cur_date > end_date:
            line = input.readline()
            continue

        output.write(','.join(line))
        line = input.readline()

    input.close()
    output.close()


def sample_part_files(input_directory, output_directory):
    """
    Extract part data using sample_single_file
    :param input_directory: input directory
    :param output_directory: output directory
    :return: None
    """

    sample_files = ['601988', '601318', '601398',  # financial
                    '601766', '601668', '601390', '600325', '600868',
                    '300059', '002594', '300033', '300104', '300024', '300120',
                    '000046', '000898', '000539', '000793', '002292', '000156']  # 2015.09.02

    for file in sample_files:
        input_filename = input_directory + file + '.txt'
        output_filename = output_directory + file + '.txt'
        print('processing: ', input_filename, '===>', output_filename)
        sample_single_file(input_filename, output_filename)


def main():
    sample_part_files('../data/normalized_data/', '../data/timeline_data/')


if __name__ == '__main__':
    main()
