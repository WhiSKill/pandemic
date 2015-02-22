import networkx as nx
import sys
import os
import matplotlib.pyplot as plot
import json

if len(sys.argv) != 3:
    print "Usage: python %s INPUT_GRAPH INPUT_NODE_CHOICES" % sys.argv[0]
    sys.exit(1)
graph_filename = os.path.basename(sys.argv[1])
print graph_filename
print sys.argv[1]
fn_parts = graph_filename.split('.')
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

def plot_graph(G):
    plot.figure(num=None, figsize=(20, 20), dpi=100)
    plot.axis('off')
    fig = plot.figure(1)
    pos = nx.spring_layout(G, iterations = 250)
    nx.draw_networkx_nodes(G, pos)
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos)

    plot.show()
    return fig

graph_fig = plot_graph(G)
