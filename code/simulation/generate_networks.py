import networkx as nx
import random
import csv
import numOfSolutionsDepthC
from itertools import combinations, groupby
import matplotlib.pyplot as plt
import os

def gnp_random_connected_graph(n, p):
    """
    Generates a random undirected graph, similarly to an Erdős-Rényi 
    graph, but enforcing that the resulting graph is conneted
    """
    edges = combinations(range(n), 2)
    G = nx.Graph()
    G.add_nodes_from(range(n))
    if p <= 0:
        return G
    if p >= 1:
        return nx.complete_graph(n, create_using=G)
    for _, node_edges in groupby(edges, key=lambda x: x[0]):
        node_edges = list(node_edges)
        random_edge = random.choice(node_edges)
        G.add_edge(*random_edge)
        for e in node_edges:
            if random.random() < p:
                G.add_edge(*e)
    return G

def main():
    for n in range(5, 21): # Creating graphs of size 5 to 20 nodes
        path = '../../data/networks/random_' + str(n)
        if not os.path.exists(path):
            os.makedirs(path)
        
        for k in range(500):
            # small world with shortcuts
            n = 42
            kk = 4
            p = 0.0
            shortcuts = 2 #6
            while 1:
                G = nx.connected_watts_strogatz_graph(n, kk, p)
                C = {}
                for gn in list(G.nodes()):
                    C[gn] = CMAP[gn%(kk-1)]

                edges = list(G.edges())
                RE = random.sample(edges, shortcuts)

                lst = []
                for re in RE:
                    lst.append(re[0])
                    lst.append(re[1])
                    G.remove_edge(re[0], re[1])

                while lst:
                    rand1 = pop_random(lst)
                    rand2 = pop_random(lst)
                    G.add_edge(rand1, rand2)

                cp = numOfSolutionsDepthC.getNumOfSolutions(G)
                if cp == 6:
                    break;
            
            # plt.figure(figsize=(8,5))
            # nx.draw(G, node_color='lightblue', with_labels=True, node_size=500)
            # plt.show()
            
            nx.write_edgelist(G, '../../data/networks/sw_shortcut2/sw_shortcut2_2_' + str(k) +'.edgelist', data=False)

            # pref attachemnt
            # n = 10
            # G = nx.barabasi_albert_graph(n, 2) #3
            # nx.write_edgelist(G, '../../data/networks/small_pa_2/pa_2_2_' + str(k) +'.edgelist', data=False)
            
            # random connected networks
            # probability = 0.05
            # G = gnp_random_connected_graph(n, probability)
                
            # plt.figure(figsize=(8,5))
            # nx.draw(G, node_color='lightblue', with_labels=True, node_size=500)
            # plt.show()

            # nx.write_edgelist(G, path + '/random_' + str(n) + '_' + str(k) +'.edgelist', data=False)

if __name__ == "__main__":
    main()