import networkx as nx
import random
import numpy as np
import csv
import matplotlib.pyplot as plt
import os

import numOfSolutionsDepthC
import divisionGame

# # t_file = csv.writer(open("../../data/data_trial_lattice_kk3.csv", "w"))
# s_file = csv.writer(open("../../data/data_summary_lattice_kk3.csv", "w"))
# # t_file.writerows([["size", "ave_rate", "density", "clustering", "shortest_path", "std_rate", "median_rate"]])
# s_file.writerows([["size", "ave_rate", "ave_density", "ave_clustering", "ave_shortest_path", "ave_std_rate", "ave_median_rate"]])

# kk = 4 # number of connections per node
p = 0.0 # rewiring probability
th = 0 # 100000 # threshohold that represents storage capacity
max_steps = 5000

def run_simulations(G, n, num_trials):
    Rate = []
    steps = []

    D = {}
    for gn in list(G.nodes()):
        D[gn] = 0

    # Initialize node color for 3 items
    cycls_3 = [c for c in nx.cycle_basis(G) if len(c)==3]

    for _ in range(num_trials):
        if not cycls_3:
            print("N:" + str(n) + ", couldn't find a cycle")
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

        incomp_nodes = divisionGame.runWithDL3(G, D, th)
        Rate.append(1.0 * incomp_nodes[-1] / n) # DoL function returns array w/ # of incomplete nodes

        # Check if there are any non-empty (non-zero) elements in the array
        if np.any(incomp_nodes != 0):
            # Find the last non-empty index (index of the last non-zero value)
            steps.append(np.max(np.nonzero(incomp_nodes)[0]) + 1)
        else:
            steps.append(max_steps)
    
    return Rate, steps

def main():
    # k_file = csv.writer(open("../../data/data_lattice_single.csv", "w"))

    n = 20
    num_trials = 100
    comp_rates = []

    # Generate a network from the edgelists
    for k in range(100):
        filename = '../../data/networks/pa_2/pa_2_2_' + str(k) + '.edgelist'
        dataFile = csv.reader(open(filename, 'r'))

        G = nx.Graph()
        for data in dataFile:
            data = list(map(lambda x:x.strip(), data))
            data2 = data[0].split(" ")
            u1 = int(data2[0])
            u2 = int(data2[1])
            G.add_edge(u1, u2)
        
        print(k)
        incomp_rates, steps = run_simulations(G, n, num_trials) # Returns all trial incompletion rates, # steps
        comp_rates = comp_rates + [1 - r for r in incomp_rates]
    
    plt.hist(comp_rates, bins=25, color='blue', edgecolor='black')
    plt.xlabel('Completion Rate')
    plt.ylabel('Frequency')
    plt.title('Pref Attach w/ ' + str(n) + ' Nodes')
    plt.show()


if __name__ == "__main__":
    main()
