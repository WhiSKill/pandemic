
import networkx as nx
import sys
import json
import random
import snap
import timeit

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
G_snap = snap.TUNGraph.New()
graph_json = {}
with open(sys.argv[1], 'r') as in_file:
    graph_json = json.load(in_file)
# setup SNAP graph object
for id_str in graph_json.keys():
    n_id = int(id_str)
    if not G_snap.IsNode(n_id):
        G_snap.AddNode(n_id)
    for neighbor_id_str in graph_json[id_str]:
        neighbor_id = int(neighbor_id_str)
        if not G_snap.IsNode(neighbor_id):
            G_snap.AddNode(neighbor_id)
        G_snap.AddEdge(n_id, neighbor_id)

# print basic info
snap.PrintInfo(G_snap, "Python type TUNGraph")

# get closeness centrality of all nodes
closeness_dict = {}
closeness_ht = snap.TIntFltH() # SNAP hash table
start_time = timeit.default_timer()
for node in G_snap.Nodes():
    closeness_ht.AddDat(node.GetId(), snap.GetClosenessCentr(G_snap, node.GetId()))
    closeness_dict[node.GetId()] = snap.GetClosenessCentr(G_snap, node.GetId())
elapsed = timeit.default_timer() - start_time
print elapsed

sorted_closeness = sortDictKeys(closeness_dict)
top_closeness = sorted_closeness[1 : (2*num_seeds)]

#print "Number of best choices: " + str(len(top_btwn))
out_filename = fn_parts[0] + '.' + fn_parts[1] + '.' + fn_parts[2] + '_closeness_sub'
with open(out_filename, 'w') as out_file:
    for i in range(50):
        round = [top_closeness[i] for i in sorted(random.sample(xrange(len(top_closeness)), num_seeds))]
        for node in round:
            out_file.write(str(node) + '\n')



"""
top_closeness_vec = snap.TIntV()
for id in top_closeness:
    top_closeness_vec.Add(id)

# create neighbor vector
neighbors_vec = snap.TIntV()

top_n_closeness = 5
# iterate over all top closeness nodes to get neighbors
for i in range(top_n_closeness):
    curr_node_id = top_closeness[i]
    for node_id in top_closeness[i+1 : top_n_closeness]:
        # get common neighbors
        curr_vec = snap.TIntV()
        snap.GetCmnNbrs(G_snap, curr_node_id, node_id, curr_vec)
        neighbors_vec.Union(curr_vec)
# make vector of id's a set
neighbors_vec.Merge()
# get all neighbors that are not in top closeness
neighbors_vec.Diff(top_closeness_vec)
for id in neighbors_vec:
    print id

"""

"""
for node in closeness:
    print "node: %d centrality: %f" % (node, closeness[node])



# remove singletons
G.remove_nodes_from(nx.isolates(G))
num_nodes = nx.number_of_nodes(G)

print "Nodes: " + str(num_nodes)
print "Seeds: " + str(num_seeds)
# get degree centrality of all nodes and sort by key
deg_centrality = nx.degree_centrality(G)
deg_centrality_sorted = sortDictKeys(deg_centrality)
top_deg = deg_centrality_sorted[1:min(3*num_seeds, num_nodes)]
"""




"""
# get core number of nodes
core_num = nx.core_number(G)
core_num_sorted = sortDictKeys(core_num)
max_core = core_num[core_num_sorted[1]]
print "Max Core: " + str(max_core)


k_num = max_core - 1
kshell_nodes = []
while len(kshell_nodes) < num_seeds:
    kshell_nodes = list(set(kshell_nodes) | set(nx.nodes(nx.k_shell(G, k=k_num, core_number=core_num))))
    print "Num in " + str(k_num) + "-shell: " + str(len(kshell_nodes))
    k_num -= 1
print kshell_nodes

maxshell_nodes = nx.nodes(nx.k_shell(G, k=max_core, core_number=core_num))
print "Num in " + str(max_core) + "-shell: " + str(len(maxshell_nodes))


# select nodes that are in all top lists
best_nodes = []
for node_id in maxshell_nodes:
    if node_id in top_deg or node_id in top_btwn:
        best_nodes.append(node_id)

"""

"""
# get betweeness centrality and sort by key
if num_nodes < 750:
    btwn_centrality = nx.betweenness_centrality(G)
else:
    btwn_centrality = nx.betweenness_centrality(G, 750)
btwn_sorted = sorted(btwn_centrality.keys(), key=lambda k: btwn_centrality[k], reverse=True)
top_btwn = btwn_sorted[1:min(2*num_seeds, num_nodes)]


"""