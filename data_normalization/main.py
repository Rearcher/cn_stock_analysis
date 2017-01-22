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
from utils.date_util import get_date_ruler


def main():
    log_config('../logs/all.log')

    # first step
    # if os.path.exists('../data/normalized_data'):
    #     shutil.rmtree('../data/normalized_data')
    # os.mkdir('../data/normalized_data')
    # normalize_all_file_parallel('../data/A_history_data', '../data/normalized_data', 8)

    # second step
    # if os.path.exists('../data/aligned_data'):
    #     shutil.rmtree('../data/aligned_data')
    # os.mkdir('../data/aligned_data')
    # date_ruler = get_date_ruler('2015-01-05', '2015-11-02')
    # align_all_file_parallel('../data/normalized_data', '../data/aligned_data', date_ruler, cores=8, fake_limit=1000)

    # third step
    # if os.path.exists('../data/returned_data'):
    #     shutil.rmtree('../data/returned_data')
    # os.mkdir('../data/returned_data')
    # calc_all_file('../data/aligned_data', '../data/returned_data', 8)
    #
    merge_all('../data/returned_data', 7, '../data/return_all.txt')


if __name__ == '__main__':
    main()
