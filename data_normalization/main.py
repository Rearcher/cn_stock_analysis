"""The starter.

   1. execute normalize_date_format
   2. execute normalize_date_alignment
   3. execute normalize_stock_return
"""
import os
import shutil
from data_normalization.normalize_date_format import normalize_all_file_parallel
from data_normalization.normalize_date_alignment import align_all_file_parallel
from data_normalization.normalize_stock_return import calc_all_file
from data_normalization.normalize_stock_return import merge_all
from utils.log_util import log_config


def main():
    log_config('../logs/format.log')

    # first step
    shutil.rmtree('../data/normalized_data')
    os.mkdir('../data/normalized_data')
    normalize_all_file_parallel('../data/A_history_data', '../data/normalized_data')

    # second step
    shutil.rmtree('../data/aligned_data')
    os.mkdir('../data/aligned_data')
    align_all_file_parallel('../data/normalized_data', '../data/aligned_data')

    # third step
    shutil.rmtree('../data/returned_data')
    os.mkdir('../data/returned_data')
    calc_all_file('../data/aligned_data', '../data/returned_data')

    merge_all('../data/returned_data', 4, 'close_all.txt')


if __name__ == '__main__':
    main()
