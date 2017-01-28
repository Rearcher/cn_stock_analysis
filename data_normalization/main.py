"""The starter.

   1. execute normalize_date_format
   2. execute normalize_date_alignment
   3. execute normalize_stock_return
"""
import os
import shutil

from data_normalization.normalize_date_alignment import align_all_file_parallel
from data_normalization.normalize_date_format import normalize_all_file_parallel
from utils.date_util import get_date_ruler
from utils.log_util import log_config


def main():
    log_config('../logs/all.log')
    working_dir = '/home/rahul/tmp/data/'
    dir_0 = working_dir + 'A_history_data'

    # first step
    dir_1 = working_dir + 'normalized_data'
    if os.path.exists(dir_1):
        shutil.rmtree(dir_1)
    os.mkdir(dir_1)
    normalize_all_file_parallel(dir_0, dir_1, cores=8)

    # second step
    dir_2 = working_dir + 'aligned_data'
    if os.path.exists(dir_2):
        shutil.rmtree(dir_2)
    os.mkdir(dir_2)
    date_ruler = get_date_ruler('2015-01-05', '2015-11-02')
    align_all_file_parallel(dir_1, dir_2, date_ruler, cores=8, fake_limit=40)


if __name__ == '__main__':
    main()
