import networkx as nx
import random
import numpy as np
import csv

import numOfSolutionsDepthC
import divisionGame


ofile = csv.writer(open("../../data/data_small_world_s0_without_storage_item3.csv", "w"))
#ofile = csv.writer(open("../../data/data_small_world_s0_without_storage_item2.csv", "w"))
#ofile = csv.writer(open("../../data/data_small_world_s0_without_storage_item4.csv", "w"))
#ofile = csv.writer(open("../../data/data_small_world_s0_with_storage_item3.csv", "w"))
ofile.writerows([["gameId", "size", "#short_cut", "#solutions", "clutering", "shortest_path", "ave_rate", "std_rate", "median_rate"]])

n = 42 # nunber of nodes
kk = 4 # number of connections per node
p = 0.0 # rewiring probability
th = 0 #100000 # threthohold that represents storage capacity

for k in range(1): #500

    # Generate a network
    G = nx.connected_watts_strogatz_graph(n, kk, p)

    cp = numOfSolutionsDepthC.getNumOfSolutions(G) # calculate solution number with chromatic number
    cluster = nx.average_clustering(G) # calculate clustering coeff
    path = nx.average_shortest_path_length(G) # calculate average shortest path length

    Rate = []
    for j in range (100):


        D = {}
        for gn in list(G.nodes()):
            D[gn] = 0

        # Initialize node color for 3 items
        # 0=generalization, 1=specialization of item1, 2=specialization of item2, 3=specialization of item3
        cycls_3 = [c for c in nx.cycle_basis(G) if len(c)==3]
        e = random.choice(cycls_3)
        D[e[0]] = 1
        D[e[1]] = 2
        D[e[2]] = 3

        # Initialize node color for 2 items
        #e = random.choice(list(G.edges()))
        #D[e[0]] = 1
        #D[e[1]] = 2

        # Initialize node color for 4 items
        #cycls_3 = [c for c in nx.cycle_basis(G) if len(c)==3]
        #e = random.choice(cycls_3)
        #D[e[0]] = 1
        #D[e[1]] = 2
        #D[e[2]] = 3
        #max_v = 0
        #max_gn = None
        #for gn in G.nodes():
        #    if gn not in e:
        #        vv = 0
        #        for en in e:
        #            if G.has_edge(gn, en):
        #                vv += 1
        #        if vv > max_v:
        #            max_v = vv
        #            max_gn = gn
        #D[max_gn] = 4

        # Run the simulation
        rate= divisionGame.runWithDL3(G, D, th) # Division of labor game with 3 items
        #rate= divisionGame.runWithDL2(G, D, th) # Division of labor game with 2 items
        #rate= divisionGame.runWithDL4(G, D, th) # Division of labor game with 4 items

        Rate.append(rate[-1])

    # Record the data
    ofile.writerows([[k, n, 0, cp, cluster, path, np.mean(Rate), np.std(Rate), np.median(Rate)]])
