import networkx as nx
import random
import numpy as np
import csv
import matplotlib.pyplot as plt
import matplotlib
import os

import numOfSolutionsDepthC
import divisionGame

p = 0.0 # rewiring probability
th = 100000 # 0 # 100000 # threshohold that represents storage capacity
max_steps = 5000

def main():
    # # Small world connected graph
    # k = 4
    # n = 15
    # G = nx.connected_watts_strogatz_graph(n, k, p)

    # Random graph
    directory = "../../data/networks/random_20"
    filename = "random_20_0.edgelist"
    G = nx.read_edgelist(os.path.join(directory, filename), nodetype=int)

    D = {}
    for gn in list(G.nodes()):
        D[gn] = 0

    # Initialize node color for 3 items
    cycls_3 = [c for c in nx.cycle_basis(G) if len(c)==3]

    if not cycls_3:
        print("N: " + str(n) + ", couldn't find a cycle")
        # nodes = list(G.nodes())
        # random_nodes = np.random.choice(nodes, size=3, replace=False)
        # D[random_nodes[0]] = 1
        # D[random_nodes[1]] = 2
        # D[random_nodes[2]] = 3
    else:
        e = random.choice(cycls_3)
        # print(e)
        D[e[0]] = 1
        D[e[1]] = 2
        D[e[2]] = 3

    for key, value in D.items():
        if value:
            print("Node:", key, "Color:", value)
    
    # for n in G.nodes():
    #     print(n, list(G.neighbors(n)))

    # C = np.zeros(len(G.nodes()))
    # for n in G.nodes():
    #     C[n] = D[n]
    # print("C printing...")
    # for node, val in enumerate(C):
    #     print(node, val)

    # values = np.zeros(len(G.nodes()))
    # values = np.array([D.get(node, 0) for node in G.nodes()])
    # print("Values printing...")
    # for node, val in enumerate(values):
    #     print(node, val)

    # # Capture graph visualization
    # node_colors = [C[node] for node in list(G.nodes())]
    # plt.figure(figsize=(8, 6))
    # pos = nx.spring_layout(G, seed = 100)
    # nx.draw(G, pos, node_color=node_colors, cmap=matplotlib.colormaps.get_cmap('plasma'), with_labels=True)

    # Save the frame to the specified directory
    # plt.show()
    # plt.savefig("movie/initial_state.png")
    # plt.close()

    learners = [8, 15, 16]
    for learner in learners:
        is1 = 0
        is2 = 0
        is3 = 0

        if D[learner] == 1:
            is1 = 1
        elif D[learner] == 2:
            is2 = 1
        elif D[learner] == 3:
            is3 = 1

        # Updates neighbor specialization booleans
        for neighbor in list(G.neighbors(learner)):
            if D[neighbor] == 1:
                is1 = 1
            elif D[neighbor] == 2:
                is2 = 1
            elif D[neighbor] == 3:
                is3 = 1
        
        print("Node:", learner, "Status:", is1, is2, is3)

    Rate = divisionGame.runWithDL3_movie(G, D, th)
    print(Rate)

if __name__ == "__main__":
    main()
    