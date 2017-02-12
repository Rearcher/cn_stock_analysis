import os

import networkx as nx


def main():
    data_dir = '/Users/rahul/tmp/correlations'
    # files = os.listdir(data_dir)
    # print(len(files))
    G = nx.Graph()
    G.add_edge('000001', '000002', weight=0.8)
    G.add_edge('000001', '000003', weight=0.4)
    print(G.edges(data='weight'))
    print(G.nodes())


if __name__ == '__main__':
    main()
