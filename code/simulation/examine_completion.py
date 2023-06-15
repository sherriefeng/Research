import networkx as nx
import random
import numpy as np
import csv
import numOfSolutionsDepthC

ofile = csv.writer(open("../../data/data_pref_attach_2_base.csv", "w"))
ofile.writerows([["gameId", "size", "#solutions", "clustering", "shortest_path", "transitivity", "completion_rate"]])

nn = 20 # nunber of nodes

for k in range(500):

    # Generate a network from the edgelists
    filename = '../../data/networks/pa_2/pa_2_2_' + str(k) +'.edgelist'
    dataFile = csv.reader(open(filename, 'r'))

    G = nx.Graph()
    for data in dataFile:
        data = list(map(lambda x:x.strip(), data))
        data2 = data[0].split(" ")
        u1 = int(data2[0])
        u2 = int(data2[1])
        G.add_edge(u1, u2)

    cp = numOfSolutionsDepthC.getNumOfSolutions(G) # calculate solution number with chromatic number
    cluster = nx.average_clustering(G) # calculate clustering coeff
    path = nx.average_shortest_path_length(G) # calculate average shortest path length
    trans = nx.transitivity(G) # calculate transitivity

    # Calcurate the competion nodes from the division of labor perspective
    COMP = []
    for i in range(int(cp/3)):
        CD = numOfSolutionsDepthC.getSampleCombination2(G, i)
    	#print(CD)
        comp = 0
        for n in G.nodes():
            L = {1: False, 2: False, 3: False}
            L[CD[n]] = True
            for nei in G.neighbors(n):
                L[CD[nei]] = True
            if L[1] == True and L[2] == True and L[3] == True:
                comp += 1
        COMP.append(comp)

    # Record the data
    ofile.writerows([[k, n, cp, cluster, path, trans, 1.0 * np.mean(COMP) / nn]])
