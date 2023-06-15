import networkx as nx
import random
import numpy as np
import csv
import itertools

import numOfSolutionsDepthCItem4
import divisionGame

ofile = csv.writer(open("../../data/data_pref_attach_3_without_storage_item4.csv", "w"))
#ofile = csv.writer(open("../../data/data_pref_attach_3_without_storage_item3.csv", "w"))
#ofile = csv.writer(open("../../data/data_pref_attach_3_without_storage_item5.csv", "w"))
#ofile = csv.writer(open("../../data/data_pref_attach_3_with_storage_item4.csv", "w"))
ofile.writerows([["gameId", "size", "#solutions", "ave_rate", "sd_rate"]])

n = 20 # nunber of nodes
th = 0 #100000 # threthohold that represents storage capacity

for k in range(500):
    print(k)
    filename = '../../data/networks/pa_3/pa_3_2_' + str(k) +'.edgelist'
    dataFile = csv.reader(open(filename, 'r'))

    G = nx.Graph()
    for data in dataFile:
        data = list(map(lambda x:x.strip(), data))
        data2 = data[0].split(" ")
        u1 = int(data2[0])
        u2 = int(data2[1])
        G.add_edge(u1, u2)



    # Examine complete networks of 4 nodes for color initialization
    cycls_3 = [c for c in nx.cycle_basis(G) if len(c)==3]
    Cy = []
    for cy in cycls_3:
        cy2 = sorted(cy)
        Cy.append((cy2[0], cy2[1], cy2[2]))

    seq = range(n)
    Candidates = []
    for comb in itertools.combinations(seq,4):
        numTri = 0
        for comb2 in itertools.combinations(comb, 3):
            if comb2 in Cy:
                numTri += 1
        if numTri > 2:
            Candidates.append(comb)

    if len(Candidates) > 0:

        cp = numOfSolutionsDepthCItem4.getNumOfSolutions(G) # calculate solution number with chromatic number
        #cluster = nx.average_clustering(G) # calculate clustering coeff
        #path = nx.average_shortest_path_length(G) # calculate average shortest path length

        Rate = []
        for j in range (100):

            D = {}
            for gn in G.nodes():
                D[gn] = 0

            # Initialize node color for 4 items
            # 0=generalization, 1=specialization of item1, 2=specialization of item2, 3=specialization of item3, 4=specialization of item4
            e = random.choice(Candidates)
            ls = [1, 2, 3, 4]
            random.shuffle(ls)
            D[e[0]] = ls[0]
            D[e[1]] = ls[1]
            D[e[2]] = ls[2]
            D[e[3]] = ls[3]

            # Initialize node color for 3 items
            #cycls_3 = [c for c in nx.cycle_basis(G) if len(c)==3]
            #e = random.choice(cycls_3)
            #D[e[0]] = 1
            #D[e[1]] = 2
            #D[e[2]] = 3

            # Initialize node color for 5 items
            #e = random.choice(Candidates)
            #ls = [1, 2, 3, 4, 5]
            #random.shuffle(ls)
            #D[e[0]] = ls[0]
            #D[e[1]] = ls[1]
            #D[e[2]] = ls[2]
            #D[e[3]] = ls[3]
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
            #D[max_gn] = ls[4]


            # Run the simulation
            rate = divisionGame.runWithDL4(G, D, th) # Division of labor game with 4 items
            #rate = divisionGame.runWithDL3(G, D, th) # Division of labor game with 3 items
            #rate = divisionGame.runWithDL5(G, D) # Division of labor game with 5 items (only without storage capacity)

            Rate.append(1.0 * rate[-1] / n)

        # Record the data
        ofile.writerows([[k, n, cp, np.mean(Rate), np.std(Rate)]])
    else:
        ofile.writerows([[k, n, "", "", ""]])


