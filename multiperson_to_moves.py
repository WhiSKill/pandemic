import sys
import json
import os

if len(sys.argv) != 2:
    print "Usage: python %s INPUT_GRAPH" % sys.argv[0]
    sys.exit(1)

# get constants from filename
filename = os.path.splitext(sys.argv[1])[0]

with open(sys.argv[1], 'r') as in_file:
    graph_json = json.load(in_file)
# setup SNAP graph object
for id_str in graph_json.keys():
    with open(id_str + '_' + filename, 'w') as out_file:
        for l in graph_json[id_str]:
            for n in l:
                out_file.write(n + '\n')
