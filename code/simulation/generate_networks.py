import networkx as nx
import random
import csv
import numOfSolutionsDepthC

for k in range(500):
	# small world with shortcuts
	# n = 42
	# kk = 4
	# p = 0.0
	# shortcuts = 2 #6
	# while 1:
 #        G = nx.connected_watts_strogatz_graph(n, kk, p)
 #        C = {}
 #        for gn in list(G.nodes()):
 #            C[gn] = CMAP[gn%(kk-1)]

 #        edges = list(G.edges())
 #        RE = random.sample(edges, shortcuts)

 #        lst = []
 #        for re in RE:
 #            lst.append(re[0])
 #            lst.append(re[1])
 #            G.remove_edge(re[0], re[1])

 #        while lst:
 #            rand1 = pop_random(lst)
 #            rand2 = pop_random(lst)
 #            G.add_edge(rand1, rand2)

 #        cp = numOfSolutionsDepthC.getNumOfSolutions(G)
 #        if cp == 6:
 #            break;
    #nx.write_edgelist(G, '../../data/networks/sw_shortcut2/sw_shortcut2_2_' + str(k) +'.edgelist', data=False)

    #pref attachemnt
    n = 20
    G = nx.barabasi_albert_graph(n, 2) #3
    #nx.write_edgelist(G, '../../data/networks/pa_2/pa_2_2_' + str(k) +'.edgelist', data=False)