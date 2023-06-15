import networkx as nx
import numpy as np
import csv
import matplotlib.pyplot as plt
import random
import numOfSolutionsDepthC
import divisionGame

ifile1 = csv.reader(open("../../data/networks/taro_exchange.csv", 'r'))
#ifile1.next()

OG = nx.Graph()
A = {}
count = 0
for data in ifile1:
	data = list(map(lambda x:x.strip(), data))
	for i in range(0, len(data)):
		if len(data[i]) > 0 and int(data[i]) == 1:
			OG.add_edge(count, i)
	count += 1

#cp = numOfSolutionsDepthC.getNumOfSolutions(G)
#print cp
#print len(G.nodes())
#print len(G.edges())
#print nx.density(G)
#print nx.average_clustering(G)
#print nx.average_shortest_path_length(G)

#plt.figure(facecolor="white", figsize=(8,8))
#pos = nx.nx_agraph.graphviz_layout(G, prog='neato')
#nx.draw(G, pos, node_color='black', node_size=150)
#plt.show()



#Simulation
ofile = csv.writer(open("../../data/data_real_network.csv", "w"))
ofile.writerows([["group", "threshold", "num_node", "num_edge", "density", "cp", "clustering", "path_length", "#step", "rate_completion", "std_cp", "std_clustering", "str_path_length", "std_rate_completion"]])

def rewiring(OG, group):
    G = OG.copy()
    if group != "org":
        ec = 0
        nodes = list(G.nodes())
        while ec < 6:
            pair = random.sample(nodes, 2)
            if G.has_edge(pair[0], pair[1]) or G.has_edge(pair[1], pair[0]):
                if group == "minus":
                    G.remove_edge(pair[0], pair[1])
                    ec += 1
            else:
                if group == "plus":
                    G.add_edge(pair[0], pair[1])
                    ec += 1
    return G


for group in ["org", "plus", "minus"]:

    for th in [0, 1, 10000]:

        NN = []
        NE = []
        CP = []
        Density = []
        Clustering = []
        Path = []
        RR = {0:[]}
        for j in range(500):
            print(j)
            is_connected = False
            while is_connected == False:
                G = rewiring(OG, group)
                is_connected = nx.is_connected(G)

            CP.append(numOfSolutionsDepthC.getNumOfSolutions(G))
            NN.append(len(G.nodes()))
            NE.append(len(G.edges()))
            Density.append(nx.density(G))
            Clustering.append(nx.average_clustering(G))
            Path.append(nx.average_shortest_path_length(G))

            D = {}
            for gn in G.nodes():
                D[gn] = 0

            cycls_3 = [c for c in nx.cycle_basis(G) if len(c)==3]
            e = random.choice(cycls_3)
            D[e[0]] = 1
            D[e[1]] = 2
            D[e[2]] = 3

            R = divisionGame.runWithDL3(G, D, th)
            RR[0].append(len(G.nodes())*1.0-3.0)
            for i in range(3000):
                if i+1 not in RR: RR[i+1] = []
                RR[i+1].append(R[i])

        for k, v in RR.items():
            ofile.writerows([[group, th, np.mean(NN), np.mean(NE), np.mean(Density), np.mean(CP), np.mean(Clustering), np.mean(Path), k, np.mean(v), np.std(CP), np.std(Clustering), np.std(Path), np.std(v) ]])