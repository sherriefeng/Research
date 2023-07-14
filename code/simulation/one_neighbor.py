import networkx as nx
import random
import numpy as np
import csv
import oneNeighborSolutions
import numOfSolutionsDepthC

# ofile = csv.writer(open("../../data/data_pref_attach_2_base.csv", "w"))
# ofile.writerows([["gameId", "size", "#solutions", "clustering", "shortest_path", "transitivity", "completion_rate"]])

nn = 10 # number of nodes

for k in range(500):

    # Generate a network from the edgelists
    filename = '../../data/networks/small_pa_2/pa_2_2_' + str(k) +'.edgelist'
    dataFile = csv.reader(open(filename, 'r'))

    G = nx.Graph()
    for data in dataFile:
        data = list(map(lambda x:x.strip(), data))
        data2 = data[0].split(" ")
        u1 = int(data2[0])
        u2 = int(data2[1])
        G.add_edge(u1, u2)

    cp = oneNeighborSolutions.getNumOfSolutions(G) # calculate solution number with chromatic number
    print("game #:", k, "solutions:", cp)
