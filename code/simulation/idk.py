import networkx as nx
import random
import numpy as np
import csv
import numOfSolutionsDepthC

 # Generate a network from the edgelists
filename = '../../data/networks/pa_2/pa_2_2_0.edgelist'
dataFile = csv.reader(open(filename, 'r'))

G = nx.Graph()
for data in dataFile:
    data = list(map(lambda x:x.strip(), data))
    data2 = data[0].split(" ")
    u1 = int(data2[0])
    u2 = int(data2[1])
    G.add_edge(u1, u2)

# cp = numOfSolutionsDepthC.getNumOfSolutions(G) # calculate solution number with chromatic number
# cluster = nx.average_clustering(G) # calculate clustering coeff
# path = nx.average_shortest_path_length(G) # calculate average shortest path length
# trans = nx.transitivity(G) # calculate transitivity

D1 = {}
for gn in list(G.nodes()):
    D1[gn] = 0

D2 = {}
for gn in G.nodes():
    D2[gn] = 0

print(D1)
print(D2)
