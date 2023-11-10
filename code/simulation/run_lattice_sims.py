import networkx as nx
import random
import numpy as np
import csv
import matplotlib.pyplot as plt

import numOfSolutionsDepthC
import divisionGame

# # t_file = csv.writer(open("../../data/data_trial_lattice_kk3.csv", "w"))
# s_file = csv.writer(open("../../data/data_summary_lattice_kk3.csv", "w"))
# # t_file.writerows([["size", "ave_rate", "density", "clustering", "shortest_path", "std_rate", "median_rate"]])
# s_file.writerows([["size", "ave_rate", "ave_density", "ave_clustering", "ave_shortest_path", "ave_std_rate", "ave_median_rate"]])

# kk = 4 # number of connections per node
p = 0.0 # rewiring probability
th = 0 # 100000 # threshohold that represents storage capacity
num_trials = 100
max_steps = 5000

def run_simulations(G, n, num_trials):
    Rate = []
    steps = []

    D = {}
    for gn in list(G.nodes()):
        D[gn] = 0

    # Initialize node color for 3 items
    cycls_3 = [c for c in nx.cycle_basis(G) if len(c)==3]
    cent = nx.eigenvector_centrality(G, weight='weight')

    for _ in range(num_trials):
        if not cycls_3:
            print("N:", n, ", couldn't find a cycle")
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

        th = 100
        print(cent)

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
    k_file = csv.writer(open("../../data/data_all_lattice_het.csv", "w"))
    k_file.writerows([["size", "k", "ave_rate", "ave_density", "ave_clustering", "ave_shortest_path", "ave_std_rate", "ave_median_rate", "ave_incomp_nodes", "ave_steps"]])
    k = 5 # arbitrary value

    # for k in range(4, 11):
        # s_file = csv.writer(open("../../data/data_all_lattice_het" + str(k) + ".csv", "w"))
        # s_file.writerows([["size", "k", "ave_rate", "ave_density", "ave_clustering", "ave_shortest_path", "ave_std_rate", "ave_median_rate", "ave_incomp_nodes", "ave_steps"]])

    for n in range(k + 1, 51):
        summary_rates = []
        summary_density = []
        summary_cluster = []
        summary_path = []
        summary_incomp = []
        summary_steps = []

        # for _ in range(25):

        # Generate a network
        G = nx.connected_watts_strogatz_graph(n, k, p)
        
        # plt.figure(figsize=(8,5))
        # nx.draw(G, node_color='lightblue', with_labels=True, node_size=500)
        # plt.show()

        density = nx.density(G)
        cluster = nx.average_clustering(G) # calculate clustering coeff
        path = nx.average_shortest_path_length(G) # calculate average shortest path length

        trial_rates, steps = run_simulations(G, n, num_trials) # Returns all trial incompletion rates, # steps
        avg_incomp_rate = np.mean(trial_rates)
        avg_comp_rate = 1 - avg_incomp_rate
        avg_incomp_nodes = n * avg_incomp_rate
        avg_steps = np.mean(steps)

        summary_rates.append(avg_comp_rate)
        summary_density.append(density)
        summary_cluster.append(cluster)
        summary_path.append(path)
        summary_incomp.append(avg_incomp_nodes)
        summary_steps.append(avg_steps)
        
        ave_summary_rate = np.mean(summary_rates)
        print("N:", n, "K:", k, "Rate:", ave_summary_rate, "Steps:", avg_steps)

        # RECORD SUMMARY DATA TO LOCAL FILE
        # s_file.writerows([[n, k, ave_summary_rate, np.mean(summary_density), np.mean(summary_cluster), np.mean(summary_path), np.std(summary_rates), np.median(trial_rates), np.mean(summary_incomp), np.mean(summary_steps)]])
        k_file.writerows([[n, k, ave_summary_rate, np.mean(summary_density), np.mean(summary_cluster), np.mean(summary_path), np.std(summary_rates), np.median(trial_rates), np.mean(summary_incomp), np.mean(summary_steps)]])

if __name__ == "__main__":
    main()

    # for n in range(11, 15):
    #     G = nx.connected_watts_strogatz_graph(n, kk, p)
            
    #     plt.figure(figsize=(8,5))
    #     nx.draw(G, node_color='lightblue', with_labels=True, node_size=500)
    #     plt.show()

    # G = nx.connected_watts_strogatz_graph(6, 4, p)
    # plt.figure(figsize=(8,5))
    # nx.draw(G, node_color='lightblue', with_labels=True, node_size=500)
    # plt.show()
    