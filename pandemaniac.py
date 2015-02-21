import networkx as nx
import sys
import json

"""
if len(sys.argv) != 3:
    print "Usage: python %s INPUT_GRAPH OUT_FILE" % sys.argv[0]
    sys.exit(1)
"""
filename = "2.10.100"

# get constants from filename
fn_parts = filename.split('.')
if len(fn_parts) != 3:
    print "INPUT_GRAPH filename is not valid!  (num_players.num_seeds.graph_id)"
num_players = int(fn_parts[0])
num_seeds = int(fn_parts[1])

# init graph
G = nx.Graph()
graph_json = {}
with open(filename, 'r') as in_file:
    graph_json = json.load(in_file)

# add all nodes/edges
for node_id in range(len(graph_json)):
    for str_id in graph_json[str(node_id)]:
        G.add_edge(node_id, int(str_id))

"""
#articulation points

comm_btwn_centrality = nx.communicability_betweenness_centrality(G)
comm_centrality = nx.communicability_centrality(G)
eccentricities = nx.eccentricity(G)
center = nx.center(G, e=eccentricities)


print sorted(comm_btwn_centrality.values(), reverse=True)
"""
