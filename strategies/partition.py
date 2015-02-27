import sys
import os
import json
import networkx as nx
import matplotlib.pyplot as plt
from networkx.readwrite import json_graph
from random import shuffle
import matplotlib.pyplot as ply
import comm
import math
from CONFIG import NUM_GAMES

SUFFIX = "_part2"

def main(argv):

    if len(argv) !=  2:
        print 'Usage: python %s GRAPH_FILE' % argv[0]
        sys.exit(2)

    # Open graph file
    graph_path = argv[1]
    graph_name = os.path.basename(graph_path)

    tokens = graph_name.split('.')
    if not (tokens[0].isdigit() and tokens[1].isdigit()):
        print 'Error: GRAPH_FILE should be named in the following format:'
        print '       num_players.num_seeds.unique_id'
        sys.exit(2)

    with open(graph_path) as graph_file:
        graph = json.loads(graph_file.read())

    num_players = int(tokens[0])
    num_seeds = int(tokens[1])
    num_nodes = len(graph.keys())

    print "NUM_NODES: %d" % num_nodes
    print "NUM_PLAYERS: %d" % num_players
    print "NUM_SEEDS: %d" % num_seeds
    print

    # Initialize graph
    G = nx.Graph()
    G = nx.from_dict_of_lists(graph)

    # Partition the graph into separate subgraphs
    print "Partitioning the graph into subgraphs..."
    partition = comm.best_partition(G)
    num_partitions = len(set(partition.values()))
    seeds_per_part = int(math.ceil(float(num_seeds)/num_partitions))

    print "NUM_PARTITION: %d" % num_partitions
    print

    subgraphs = []
    for com in set(partition.values()):

        list_nodes = [nodes for nodes in partition.keys()\
                                        if partition[nodes] == com]
        H = nx.Graph()
        for u in list_nodes:
            H.add_node(u)
            for v in G[u]:
                if v in list_nodes:
                    H.add_node(v)
                    H.add_edge(u, v)

        subgraphs.append(H)
        #nx.draw(H)
        #plt.show()

    # Pick top closeness centrality nodes from each subgraphs
    print "Pick %d seeds per partition:" % seeds_per_part
    print "------------------------------------"

    seed_nodes = []
    count = 0

    for H in sorted(subgraphs, key=len, reverse=True):
        cc = nx.closeness_centrality(H)
        for node in  sorted(cc, key=cc.get, reverse=True)[:seeds_per_part]:
            if count < num_seeds:
                seed_nodes.append(node)
                count += 1
                print "%s: %f" % (node, cc[node])

        print "------------------------------------"

    """
    print "Pick %d seed nodes:" % num_seeds

    seed_nodes = []
    count = 0
    num_iter = 0

    while count < num_seeds:

        for H in sorted(subgraphs, key=len, reverse=True):
            cc = nx.closeness_centrality(H)

            if count < num_seeds and len(cc) > num_iter:
                node = sorted(cc, key=cc.get, reverse=True)[num_iter]
                seed_nodes.append(node)
                count += 1
                print "%s: %f" % (node, cc[node])

        num_iter += 1

    """

    # Output submission file
    with open(graph_path+SUFFIX, 'w') as sub_file:
        for i in range(NUM_GAMES):
            for node in seed_nodes:
                sub_file.write(node)
                sub_file.write("\n")

if __name__ == "__main__":
    main(sys.argv)
