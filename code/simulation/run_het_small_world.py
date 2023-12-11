import networkx as nx
import random
import numpy as np
import csv
import sys
import os
import matplotlib.pyplot as plt

import numOfSolutionsDepthC
import divisionGame

p = 0.0 # rewiring probability
th = 0 # 100000 # threshohold that represents storage capacity
num_trials = 5 # 20
max_steps = 1000 # 5000

def run_simulations_het(G, n, num_trials):
    Rate = []
    steps = []
    n_completeness = []
    l1_norms = []
    l2_norms = []

    D = {}
    for gn in list(G.nodes()):
        D[gn] = 0

    # Initialize node color for 3 items
    cycls_3 = [c for c in nx.cycle_basis(G) if len(c)==3]
    
    th = nx.eigenvector_centrality(G, weight='weight')

    for _ in range(num_trials):
        if not cycls_3:
            # print("N:", n, ", couldn't find a cycle")
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

        # incomp_nodes, neighborhood_missing_colors = divisionGame.run_opt_DL3_het(G, D, th) # runWithDL3_het(G, D, th)
        incomp_nodes, neighborhood_missing_colors = divisionGame.runWithDL3_mod(G, D, th)

        Rate.append(1.0 * incomp_nodes[-1] / n) # DoL function returns array w/ # of incomplete nodes
        neighborhood_metrics = neighborhood_missing_colors / 3.0
        # print(neighborhood_metrics)

        n_completeness.append(np.sum(neighborhood_metrics)) # *** weighted sum?
        l1_norms.append(np.linalg.norm(neighborhood_metrics, ord=1))
        l2_norms.append(np.linalg.norm(neighborhood_metrics, ord=2))

        # Check if there are any non-empty (non-zero) elements in the array
        if np.any(incomp_nodes != 0):
            # Find the last non-empty index (index of the last non-zero value)
            steps.append(np.max(np.nonzero(incomp_nodes)[0]) + 1)
        else:
            steps.append(max_steps)
    
    return Rate, steps, n_completeness, l1_norms, l2_norms

def main():
    # k_file = csv.writer(open("../../data/data_all_pref_attach_het.csv", "w"))
    # k_file = csv.writer(open("../../data/data_all_random_avg_detail.csv", "w"))
    sum_file = csv.writer(open("../../data/random/data_all_random_avg.csv", "w"))
    sum_file.writerows([["size", "k", "avg_rate", "density", "clustering", "shortest_path", "std_rate", "median_rate", "n_comp_nodes",  "avg_steps", "avg_l1", "avg_l2"]])

    # for n in range(5, 201, 10): # Creating graphs of size 5 to 200 nodes, step 10
    #     path = '../../data/random/random_' + str(n)
    #     if not os.path.exists(path):
    #         os.makedirs(path)

    for i in range(5, 200, 10):
        folder_path = '../../data/random/random_' + str(i)
        
        # 10 different graphs per size
        for k in range(10):

            # File path for this graph's data
            out_file_path = folder_path + "/random_" + str(i) + '_' + str(k) + ".csv"
            k_file = csv.writer(open(out_file_path, "w"))
            k_file.writerows([["size", "trial", "rate", "density", "clustering", "shortest_path", "n_comp_nodes",  "steps", "l1", "l2"]])

            # File path for this graph's edgelist
            edgelist_filename = '../../data/networks/random/random_' + str(i) + '/random_' + str(i) + '_' + str(k) + '.edgelist'
            dataFile = csv.reader(open(edgelist_filename, 'r'))

            G = nx.Graph()
            for data in dataFile:
                data = list(map(lambda x:x.strip(), data))
                data2 = data[0].split(" ")
                u1 = int(data2[0])
                u2 = int(data2[1])
                G.add_edge(u1, u2)

            density = nx.density(G)
            cluster = nx.average_clustering(G)
            path = nx.average_shortest_path_length(G)
            
            # Run simulation -- returns all trial incompletion rates, # steps, node color completion metric
            try:
                trial_rates, steps, n_comp, l1_norms, l2_norms = run_simulations_het(G, i, num_trials)
            except KeyboardInterrupt:
                print("Interrupted")
                sys.exit(0)
            except:
                trial_rates, steps, n_comp = 0, 0, 0
                print("Sim failed")

            # Record trial metrics
            for t in range(num_trials):
                k_file.writerows([[i, t, 1 - trial_rates[t], density, cluster, path, n_comp[t], steps[t], l1_norms[t], l2_norms[t]]])
            
            # Calculate summary metrics
            avg_incomp_rate = np.mean(trial_rates)
            avg_comp_rate = 1 - avg_incomp_rate
            std_rate = np.std(trial_rates)
            median_rate = np.median(trial_rates)
            avg_steps = np.mean(steps)
            avg_n_comp = np.mean(n_comp)
            avg_l1 = np.mean(l1_norms)
            avg_l2 = np.mean(l2_norms)
            
            # Record summary metrics
            print("N:", i, "\tRate:%.3f " % avg_comp_rate, "\tN_Comp:%.3f " % avg_n_comp, "\tSteps:", avg_steps)
            sum_file.writerows([[i, k, avg_comp_rate, density, cluster, path, std_rate, median_rate, avg_n_comp, avg_steps, avg_l1, avg_l2]])


if __name__ == "__main__":
    main()