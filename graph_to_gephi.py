import sys
import json
import os

if len(sys.argv) != 2:
    print "Usage: python %s INPUT_GRAPH" % sys.argv[0]
    sys.exit(1)

# get constants from filename
filename = os.path.basename(sys.argv[1])
fn_parts = filename.split('.')
if len(fn_parts) != 4:
    print "INPUT_GRAPH filename is not valid!  num_players.num_seeds.graph_id.json"
    sys.exit(1)
num_players = int(fn_parts[0])
num_seeds = int(fn_parts[1])
graph_id = int(fn_parts[2])

with open(filename) as f:
    data = json.load(f)
with open('gephi_' + str(num_players) + str(num_seeds) +\
          str(graph_id) + '.csv', 'w') as f:
    for k, v in data.iteritems():
        str = k + ";" + ";".join(v)
        print >> f, str
