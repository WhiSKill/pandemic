import sys
import os
import sim
import json
import pprint
from CONFIG import NUM_GAMES

pp = pprint.PrettyPrinter(indent=1)

def main(argv):

    # Check validity of command line arguments
    if len(argv) <  4:
        print 'Usage: python %s GRAPH_FILE STRATEGY1 STRATEGY2...' % argv[0]
        sys.exit(2)

    graph_path = argv[1]
    player_paths = argv[2:]

    graph_name = os.path.basename(graph_path)

    tokens = graph_name.split('.')
    if not (tokens[0].isdigit() and tokens[1].isdigit()):
        print 'Error: GRAPH_FILE should be named in the following format:'
        print '       num_players.num_seeds.unique_id'
        sys.exit(2)


    # Set game parameters

    # Load graph
    with open(graph_path) as graph_file:
        graph = json.loads(graph_file.read())

    # Load players
    players = {}
    num_players = int(tokens[0])
    num_seeds = int(tokens[1])

    print "NUM_PLAYERS: %d" % num_players
    print "NUM_SEEDS: %d" % num_seeds
    print

    for player_path in player_paths:
        num_lines = sum(1 for line in open(player_path))
        if num_lines != NUM_GAMES * num_seeds:
            print "Error: Number of lines in %s is not %d"\
                % (player_path, (NUM_GAMES * num_seeds))
            sys.exit(2)

        # Each player file has (games * num_seeds) lines
        with open(player_path) as player_file:
            player_name = os.path.basename(player_path)
            player_seeds = []

            for i in range(NUM_GAMES):
                seeds = []

                for j in range(num_seeds):
                    seeds.append(player_file.readline().strip())

                player_seeds.append(seeds)

            # Add a player to the list
            players[player_name] = player_seeds

    # Print out the results
    print "===========RESULTS==========="
    results = sim.run(graph, players, NUM_GAMES)
    #pp.pprint(results)
    for result in results:
        print result[0]

if __name__ == "__main__":
    main(sys.argv)
