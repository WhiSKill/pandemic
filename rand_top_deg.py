
import networkx as nx
import sys
import json
import random

# input a dict; output keys sorted in descending order
def sortDictKeys(dict):
    return sorted(dict.keys(), key=lambda k: dict[k], reverse=True)


if len(sys.argv) != 2:
    print "Usage: python %s INPUT_GRAPH" % sys.argv[0]
    sys.exit(1)

# get constants from filename
fn_parts = sys.argv[1].split('.')
if len(fn_parts) != 4:
    print "INPUT_GRAPH filename is not valid!  num_players.num_seeds.graph_id.json"
    sys.exit(1)
num_players = int(fn_parts[0])
num_seeds = int(fn_parts[1])

# init graph
G = nx.Graph()
graph_json = {}
with open(sys.argv[1], 'r') as in_file:
    graph_json = json.load(in_file)

# add all nodes/edges
G = nx.from_dict_of_lists(graph_json)
# remove singletons
G.remove_nodes_from(nx.isolates(G))
num_nodes = nx.number_of_nodes(G)

print "Nodes: " + str(num_nodes)
print "Seeds: " + str(num_seeds)
# get degree centrality of all nodes and sort by key
deg_centrality = nx.degree_centrality(G)
deg_centrality_sorted = sortDictKeys(deg_centrality)
top_deg = deg_centrality_sorted[1:min(2*num_seeds, num_nodes)]

out_filename = fn_parts[0] + '.' + fn_parts[1] + '.' + fn_parts[2] + '_topdeg_sub'
with open(out_filename, 'w') as out_file:
    for i in range(50):
        round = [top_deg[i] for i in sorted(random.sample(xrange(len(top_deg)), num_seeds))]
        for node in round:
            out_file.write(node + '\n')
