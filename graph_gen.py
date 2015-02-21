#!/usr/bin/python

import sys
import random
import json


if len(sys.argv) != 3:
    print "Usage: python %s NUM_NODES OUT_FILE" % sys.argv[0]
    sys.exit(1)

NUM_NODES = int(sys.argv[1])

# init a dictionary to store nodes and edges
graph = {}

for i in range(NUM_NODES):
    # generate neighbors and store in dict
    neighbors = random.sample(str(range(50)).strip('[]').split(', '), random.randrange(50))
    graph[str(i)] = neighbors

# output to file
with open(sys.argv[2], 'w') as out_file:
    json.dump(graph, out_file, indent=None)