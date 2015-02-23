"""
Choose nodes with highest closeness centralities.

Input   : A graph file named in the following way:
            num_players.num_seeds.unique_id
Output  : A text file with (num_games * num_seeds) lines.
"""
import sys
import os
import json
import networkx as nx
import matplotlib.pyplot as plt
from networkx.readwrite import json_graph
from random import shuffle

NUM_GAMES = 1
SUFFIX = "_cc"

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
    for u in graph:
        for v in graph[u]:
            G.add_node(u)
            G.add_node(v)
            G.add_edge(u, v)

    # Select nodes with higest degree centrality
    seed_nodes = []
    dc = nx.closeness_centrality(G)

    print "Top %d cadidate nodes:" % (num_seeds)
    for node in sorted(dc, key=dc.get, reverse=True)[:num_seeds]:
        seed_nodes.append(node)
        print "%s: %f" % (node, dc[node])

    # Output submission file
    with open(graph_path+SUFFIX, 'w') as sub_file:
        for i in range(NUM_GAMES):
            for node in seed_nodes:
                sub_file.write(node)
                sub_file.write("\n")

if __name__ == "__main__":
    main(sys.argv)
