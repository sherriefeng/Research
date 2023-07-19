import os
import networkx as nx
import random
import numpy as np
import csv
import numOfSolutionsDepthC
import divisionGame

th = 0 # property threshold

t_file = csv.writer(open("data_trial_random.csv", "w"))
s_file = csv.writer(open("data_summary_random.csv", "w"))
t_file.writerows([["size", "gameId", "ave_rate", "sd_rate"]])
s_file.writerows([["size", "ave_rate", "sd_rate"]])

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
    
    return Rate

def main():
    for n in range(5, 21): # Loop over graphs of size 5 to 20 nodes
        directory = "../../data/networks/random_" + str(n)
        summary_rates = []

        for k, filename in enumerate(os.listdir(directory)):
            if filename.endswith(".edgelist") and k < 100: # Can adjust upper limit on k (graph #) here
                print(filename)
                G = nx.read_edgelist(os.path.join(directory, filename), nodetype=int)

                # Run the count_solutions function multiple times with the same G and D
                num_trials = 50
                trial_rates = calculate_node_completion_rate(G, num_trials)
                node_completion_rate = 1 - np.mean(trial_rates)
                print("Avg node completion rate:", node_completion_rate)

                summary_rates.append(node_completion_rate)
            
            # RECORD TRIAL DATA TO LOCAL FILE HERE
            t_file.writerows([[n, k, node_completion_rate, np.std(trial_rates)]])
            
        # RECORD SUMMARY DATA TO LOCAL FILE
        s_file.writerows([[n, np.mean(summary_rates), np.std(summary_rates)]])

if __name__ == "__main__":
    main()