
import networkx as nx
import sys
import json
import random

# input a dict; output keys sorted in descending order
def sortDictKeys(dict):
    return sorted(dict.keys(), key=lambda k: dict[k], reverse=True)


if len(sys.argv) != 3:
    print "Usage: python %s INPUT_GRAPH OUT_FILE" % sys.argv[0]
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

print "Num Nodes: " + str(num_nodes)

deg_centrality = nx.degree_centrality(G)
deg_centrality_sorted = sortDictKeys(deg_centrality)
top_deg = deg_centrality_sorted[1:min(3*num_seeds, num_nodes)]


if num_nodes < 750:
    btwn_centrality = nx.betweenness_centrality(G)
else:
    btwn_centrality = nx.betweenness_centrality(G, 750)
btwn_sorted = sorted(btwn_centrality.keys(), key=lambda k: btwn_centrality[k], reverse=True)

top_btwn = btwn_sorted[1:min(2*num_seeds, num_nodes)]

best_nodes = []
for node_id in top_deg:
    if node_id in top_btwn:
        best_nodes.append(node_id)

with open(sys.argv[2], 'w') as out_file:
    for i in range(50):
        round = [best_nodes[i] for i in sorted(random.sample(xrange(len(best_nodes)), num_seeds))]
        for node in round:
            out_file.write(node + '\n')


"""
core_num = nx.core_number(G)
core_num_sorted = sortDictKeys(core_num)
max_core = core_num[core_num_sorted[1]]
print max_core




if num_nodes < 500:
    btwn_centrality = nx.betweenness_centrality(G)
else:
    btwn_centrality = nx.betweenness_centrality(G, 300)
btwn_sorted = sorted(btwn_centrality.keys(), key=lambda k: btwn_centrality[k], reverse=True)

top_btwn = btwn_sorted[1:num_nodes]

for node_id in top_btwn:
    print core_num[node_id]


disp = nx.dispersion(G)
disp_sorted = sortDictKeys(disp)
print disp_sorted

"""

"""
eccentricities = nx.eccentricity(G)
center = nx.center(G, e=eccentricities)

comm_centrality = nx.communicability_centrality_exp(G)
comm_sorted = sortDictKeys(comm_centrality)
print comm_sorted

comm_btwn_centrality = nx.communicability_betweenness_centrality(G)
comm_centrality = nx.communicability_centrality(G)

comm_btwn_sorted = sorted(comm_btwn_centrality.keys(), key=lambda k: comm_btwn_centrality[k], reverse=True)

print comm_btwn_sorted
"""



"""
closeness_centrality = nx.closeness_centrality(G)
closeness_centrality_sorted = sorted(closeness_centrality.keys(), key=lambda k: closeness_centrality[k], reverse=True)
print closeness_centrality_sorted


"""
