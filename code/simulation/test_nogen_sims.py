import networkx as nx
import random
import numpy as np
import csv
import matplotlib.pyplot as plt
import os

import numOfSolutionsDepthC
import divisionGame

p = 0.0 # rewiring probability
th = 100000 # 0 # 100000 # threshold that represents storage capacity
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
            print("N: " + str(n) + ", couldn't find a cycle")
        else:
            e = random.choice(cycls_3)
            D[e[0]] = 1
            D[e[1]] = 2
            D[e[2]] = 3

        incomp_nodes, num_steps = divisionGame.runWithDL3_nogen(G, D, th)

        Rate.append(1.0 * incomp_nodes[-1] / n) # DoL function returns array w/ # of incomplete nodes

        # Check if there are any non-empty (non-zero) elements in the array
        # if np.any(incomp_nodes != 0):
        #     # Find the last non-empty index (index of the last non-zero value)
        #     steps.append(np.max(np.nonzero(incomp_nodes)[0]) + 1)
        # else:
        #     steps.append(max_steps)
        steps.append(num_steps)
    
    return Rate, steps

def main():
    num_trials = 50
    comp_rates = []
    all_steps = []

    # pref attach
    n = 20
    for i in range(50):
        filename = '../../data/networks/pa_2/pa_2_2_' + str(i) + '.edgelist'
        G = nx.read_edgelist(filename, nodetype=int)
        
        print(i)
        incomp_rates, steps = run_simulations(G, n, num_trials) # Returns all trial incompletion rates, # steps
        comp_rates = comp_rates + [1 - r for r in incomp_rates]
        all_steps = all_steps + steps

    # # small world
    # n = 50
    # k = 4
    # # for n in range(5, 50):
    # for _ in range(25):
    #     # Generate a network
    #     G = nx.connected_watts_strogatz_graph(n, k, p)
    #     incomp_rates, steps = run_simulations(G, n, num_trials) # Returns all trial incompletion rates, # steps
    #     comp_rates = comp_rates + [1 - r for r in incomp_rates]
    #     all_steps = all_steps + steps
    
    # Random, Histogram for Completion Rates
    # plt.hist(comp_rates, bins=25, color='blue', edgecolor='black')
    # plt.xlabel('Completion Rate')
    # plt.ylabel('Frequency')
    # plt.title('Random w/ ' + str(n) + ' Nodes')
    # plt.show()
    
    # # Lattice, Scatter Histogram for Completion Rates
    # unique_values, frequencies = np.unique(comp_rates, return_counts=True)
    # for val, freq in zip(unique_values, frequencies):
    #     print("Completion Rate:", val, "Frequency:", freq)

    # # Lattice, Histogram for Steps
    # unique_values, frequencies = np.unique(all_steps, return_counts=True)
    # for val, freq in zip(unique_values, frequencies):
    #     print("Steps:", val, "Frequency:", freq)
    # plt.hist(all_steps, bins=100, color='blue', edgecolor='black')
    # plt.xlabel('Steps')
    # plt.ylabel('Frequency')
    # # plt.title('Lattice w/ 5 to 50 Nodes, ' + str(k) + ' Connections Per Node')
    # plt.title('Lattice w/ ' + str(n) + ' Nodes, ' + str(k) + ' Connections Per Node')
    # plt.show()

    # Pref Attach, Scatter Histogram for Completion Rates
    plt.hist(comp_rates, bins=25, color='blue', edgecolor='black')
    plt.xlabel('Completion Rate')
    plt.ylabel('Frequency')
    plt.title('Pref Attach w/ ' + str(n) + ' Nodes')
    # plt.show()
    plt.savefig("pref_attach_th_rates.png")
    plt.close()

    # Pref Attach, Histogram for Steps
    unique_values, frequencies = np.unique(all_steps, return_counts=True)
    for val, freq in zip(unique_values, frequencies):
        print("Steps:", val, "Frequency:", freq)

    plt.hist(all_steps, bins=100, color='blue', edgecolor='black')
    plt.xlabel('Steps')
    plt.ylabel('Frequency')
    plt.title('Pref Attach w/ ' + str(n) + ' Nodes')
    # plt.show()
    plt.savefig("pref_attach_th_steps.png")
    plt.close()


if __name__ == "__main__":
    main()