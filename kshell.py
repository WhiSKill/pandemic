
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
top_deg = deg_centrality_sorted[1:min(3*num_seeds, num_nodes)]

# get core number of nodes
core_num = nx.core_number(G)
core_num_sorted = sortDictKeys(core_num)
max_core = core_num[core_num_sorted[1]]
print "Max Core: " + str(max_core)

"""
k_num = max_core - 1
kshell_nodes = []
while len(kshell_nodes) < num_seeds:
    kshell_nodes = list(set(kshell_nodes) | set(nx.nodes(nx.k_shell(G, k=k_num, core_number=core_num))))
    print "Num in " + str(k_num) + "-shell: " + str(len(kshell_nodes))
    k_num -= 1
print kshell_nodes
"""

maxshell_nodes = nx.nodes(nx.k_shell(G, k=max_core, core_number=core_num))
print "Num in " + str(max_core) + "-shell: " + str(len(maxshell_nodes))

# get betweeness centrality and sort by key
if num_nodes < 750:
    btwn_centrality = nx.betweenness_centrality(G)
else:
    btwn_centrality = nx.betweenness_centrality(G, 750)
btwn_sorted = sorted(btwn_centrality.keys(), key=lambda k: btwn_centrality[k], reverse=True)
top_btwn = btwn_sorted[1:min(2*num_seeds, num_nodes)]


# select nodes that are in all top lists
best_nodes = []
for node_id in maxshell_nodes:
    if node_id in top_deg or node_id in top_btwn:
        best_nodes.append(node_id)

print "Number of best choices: " + str(len(best_nodes))
out_filename = fn_parts[0] + '.' + fn_parts[1] + '.' + fn_parts[2] + '_kshell_sub'
with open(out_filename, 'w') as out_file:
    for i in range(50):
        round = [best_nodes[i] for i in sorted(random.sample(xrange(len(best_nodes)), num_seeds))]
        for node in round:
            out_file.write(node + '\n')
