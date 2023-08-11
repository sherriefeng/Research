import networkx as nx
import random
import numpy as np
import csv
import matplotlib.pyplot as plt
import os

import numOfSolutionsDepthC
import divisionGame

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
    # o_file = csv.writer(open("../../data/data_lattice_single.csv", "w"))
    # o_file.writerows([["size", "ave_rate", "sd_rate"]])

    num_trials = 100
    comp_rates = []
    all_steps = []

    # # pref attach
    # for n in range(100):
    #     filename = '../../data/networks/pa_2/pa_2_2_' + str(n) + '.edgelist'
    #     G = nx.read_edgelist(filename, nodetype=int)
        
    #     print(k)
    #     incomp_rates, steps = run_simulations(G, n, num_trials) # Returns all trial incompletion rates, # steps
    #     comp_rates = comp_rates + [1 - r for r in incomp_rates]
    #     all_steps = all_steps + steps

    # small world
    n = 50
    k = 4
    for _ in range(25):
        # Generate a network
        G = nx.connected_watts_strogatz_graph(n, k, p)

        # density = nx.density(G)
        # cluster = nx.average_clustering(G) # calculate clustering coeff
        # path = nx.average_shortest_path_length(G) # calculate average shortest path length

        incomp_rates, steps = run_simulations(G, n, num_trials) # Returns all trial incompletion rates, # steps
        comp_rates = comp_rates + [1 - r for r in incomp_rates]
        all_steps = all_steps + steps
    
    # Random, Histogram for Completion Rates
    # plt.hist(comp_rates, bins=25, color='blue', edgecolor='black')
    # plt.xlabel('Completion Rate')
    # plt.ylabel('Frequency')
    # plt.title('Random w/ ' + str(n) + ' Nodes')
    # plt.show()
    
    # Lattice, Scatter Histogram for Completion Rates
    unique_values, frequencies = np.unique(comp_rates, return_counts=True)
    for val, freq in zip(unique_values, frequencies):
        print("Completion Rate:", val, "Frequency:", freq)
    plt.scatter(unique_values, frequencies, marker='o', s=20, color='blue')
    # plt.xlim(0.95, 1.0)
    plt.xlabel('Completion Rate')
    plt.ylabel('Frequency')
    # plt.title('Lattice w/ ' + str(n) + ' Nodes, ' + str(k) + ' Connections Per Node')
    plt.title('Lattice w/ 5 to 25 Nodes, ' + str(k) + ' Connections Per Node')
    plt.show()

    # Lattice, Histogram for Steps
    # unique_values, frequencies = np.unique(all_steps, return_counts=True)
    # for val, freq in zip(unique_values, frequencies):
    #     print("Steps:", val, "Frequency:", freq)

    # plt.hist(all_steps, bins=100, color='blue', edgecolor='black')
    # plt.xlabel('Steps')
    # plt.ylabel('Frequency')
    # plt.title('Lattice w/ ' + str(n) + ' Nodes, ' + str(k) + ' Connections Per Node')
    # plt.show()


if __name__ == "__main__":
    main()
    