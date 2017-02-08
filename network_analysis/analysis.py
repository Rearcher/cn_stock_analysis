import os

import networkx as nx


def main():
    data_dir = '/Users/rahul/tmp/correlations'
    files = os.listdir(data_dir)
    print(len(files))


if __name__ == '__main__':
    main()
