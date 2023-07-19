import os
import networkx as nx
import random
import numpy as np
import csv
import numOfSolutionsDepthC
import divisionGame

th = 0 # property threshold

ofile = csv.writer(open("data_dl_random.csv", "w"))
ofile.writerows([["gameId", "size", "ave_rate", "sd_rate"]])


def calculate_node_completion_rate(G, num_trials):
    total_nodes = len(G.nodes())
    Rate = []

    D = {}
    for gn in list(G.nodes()):
        D[gn] = 0

    # Initialize node color for 3 items
    cycls_3 = [c for c in nx.cycle_basis(G) if len(c)==3]
    if not cycls_3:
        nodes = list(G.nodes())
        random_nodes = np.random.choice(nodes, size=3, replace=False)
        D[random_nodes[0]] = 1
        D[random_nodes[1]] = 2
        D[random_nodes[2]] = 3
    else:
        e = random.choice(cycls_3)
        D[e[0]] = 1
        D[e[1]] = 2
        D[e[2]] = 3

    for _ in range(num_trials):
        rate = divisionGame.runWithDL3(G, D, th)
        Rate.append(1.0 * rate[-1] / total_nodes) # DoL function returns # of incomplete nodes
    
    return 1 - np.mean(Rate)

def main():
    for n in range(5, 21): # Loop over graphs of size 5 to 20 nodes
        directory = "../../data/networks/random_" + str(n)

        for k, filename in enumerate(os.listdir(directory)):
            if filename.endswith(".edgelist"):
                print(filename)
                G = nx.read_edgelist(os.path.join(directory, filename), nodetype=int)

                # Run the count_solutions function multiple times with the same G and D
                num_trials = 50
                node_completion_rate = calculate_node_completion_rate(G, num_trials)
                print("Avg node completion rate:", node_completion_rate)
            
            # RECORD DATA TO LCOAL FILE HERE
            ofile.writerows([[n, k, np.mean(node_completion_rate), np.std(node_completion_rate)]])

if __name__ == "__main__":
    main()