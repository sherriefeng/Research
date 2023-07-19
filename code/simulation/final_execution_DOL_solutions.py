# # the version of the code with new G and D generated every time
# import divisionGame_ann_commented
# import networkx as nx
# import random
# import numpy as np
# import csv
# import numOfSolutionsDepthC
# import divisionGame

# ofile = csv.writer(open("../../data/data_pref_attach_2_without_storage_item3.csv", "w"))
# # ofile = csv.writer(open("../../data/data_pref_attach_2_without_storage_item2.csv", "w"))
# # ofile = csv.writer(open("../../data/data_pref_attach_2_without_storage_item4.csv", "w"))
# # ofile = csv.writer(open("../../data/data_pref_attach_2_with_storage_item3.csv", "w"))
# ofile.writerows([["gameId", "size", "#solutions", "ave_rate", "sd_rate"]])

# n = 20 # nunber of nodes
# th = 0 # 100000 # threshold that represents storage capacity

# for k in range(500):
#     print(k)
#     # Generate a network from the edgelists
#     filename = '../../data/networks/pa_2/pa_2_2_' + str(k) + '.edgelist'
#     dataFile = csv.reader(open(filename, 'r'))

#     G = nx.Graph()
#     for data in dataFile:
#         data = list(map(lambda x:x.strip(), data))
#         data2 = data[0].split(" ")
#         u1 = int(data2[0])
#         u2 = int(data2[1])
#         G.add_edge(u1, u2)

#     cp = numOfSolutionsDepthC.getNumOfSolutions(G) # calculate solution number with chromatic number
#     # cluster = nx.average_clustering(G) # calculate clustering coeff
#     # path = nx.average_shortest_path_length(G) # calculate average shortest path length

#     Rate = []
#     for j in range (100):

#         D = {}
#         for gn in list(G.nodes()):
#             D[gn] = 0

#         # Initialize node color for 3 items
#         # 0 = generalization, 1 = specialization of item1, 2 = specialization of item2, 3 = specialization of item3
#         cycls_3 = [c for c in nx.cycle_basis(G) if len(c)==3]
#         e = random.choice(cycls_3)
#         D[e[0]] = 1
#         D[e[1]] = 2
#         D[e[2]] = 3

#         # Initialize node color for 2 items
#         # e = random.choice(list(G.edges()))
#         # D[e[0]] = 1
#         # D[e[1]] = 2

#         # Initialize node color for 4 items
#         # cycls_3 = [c for c in nx.cycle_basis(G) if len(c)==3]
#         # e = random.choice(cycls_3)
#         # D[e[0]] = 1
#         # D[e[1]] = 2
#         # D[e[2]] = 3
#         # max_v = 0
#         # max_gn = None
#         # for gn in G.nodes():
#         #    if gn not in e:
#         #        vv = 0
#         #        for en in e:
#         #            if G.has_edge(gn, en):
#         #                vv += 1
#         #        if vv > max_v:
#         #            max_v = vv
#         #            max_gn = gn
#         # D[max_gn] = 4

#         # Run the simulation
#         rate = divisionGame.runWithDL3(G, D, th) # Division of labor game with 3 items
#         # rate = divisionGame.runWithDL2(G, D, th) # Division of labor game with 2 items
#         # rate = divisionGame.runWithDL4(G, D, th) # Division of labor game with 4 items

#         Rate.append(1.0 * rate[-1] / n)

#     # Record the data
#     ofile.writerows([[k, n, cp, np.mean(Rate), np.std(Rate)]])

# # def count_solutions(num_trials):
# #     solution_counts = {}

# #     for _ in range(num_trials):
# #         # result = divisionGame_ann_commented._runWithDL3(Nodes, Neighbors, C, A, h)
# #         result = divisionGame_ann_commented.runWithDL3(G, D, th)
      
# #         #Check if division of labor was achieved
# #         if result[-1] == 0:  # Division of labor was achieved
            
# #             solution = tuple(C)  # Snapshot of the current solution

# #             if solution in solution_counts:
# #                 solution_counts[solution] += 1
# #             else:
# #                 solution_counts[solution] = 1

# #     return solution_counts

# def count_solutions(num_trials):
#     solution_counts = 0

#     for _ in range(num_trials):
#         # result = divisionGame_ann_commented._runWithDL3(Nodes, Neighbors, C, A, h)
#         result = divisionGame_ann_commented.runWithDL3(G, D, th)
      
#         #Check if division of labor was achieved
#         if result[-1] == 0:  # Division of labor was achieved
#             print("achieve DOL")
#             solution_counts += 1
 

#     return solution_counts

# # you can now use the functions from the division_labor module
# num_trials = 100
# solution_counts = count_solutions(num_trials)
# print(solution_counts)

##################################################################################################################################

# only construct G and D once and use them in multiple runs of count_solutions
# count_solutions function has been altered to accept G and D as arguments

# import copy
# import divisionGame_ann_commented
# import networkx as nx
# import random
# import numpy as np
# import csv
# import numOfSolutionsDepthC
# import divisionGame

# ofile = csv.writer(open("../../data/data_pref_attach_2_without_storage_item3.csv", "w"))
# ofile.writerows([["gameId", "size", "#solutions", "ave_rate", "sd_rate"]])

# n = 20 # number of nodes
# th = 0 # threshold that represents storage capacity

# filename = '../../data/networks/pa_2/pa_2_2_' + str(0) + '.edgelist'  # Replace '0' with appropriate value
# dataFile = csv.reader(open(filename, 'r'))

# G = nx.Graph()
# for data in dataFile:
#     data = list(map(lambda x:x.strip(), data))
#     data2 = data[0].split(" ")
#     u1 = int(data2[0])
#     u2 = int(data2[1])
#     G.add_edge(u1, u2)

# D = {}
# for gn in list(G.nodes()):
#     D[gn] = 0

# # Initialize node color for 3 items
# cycls_3 = [c for c in nx.cycle_basis(G) if len(c)==3]
# e = random.choice(cycls_3)
# D[e[0]] = 1
# D[e[1]] = 2
# D[e[2]] = 3

# def count_solutions(G, D, num_trials):
#     solution_counts = 0

#     for _ in range(num_trials):
#         G_copy = copy.deepcopy(G)
#         D_copy = copy.deepcopy(D)
#         result = divisionGame_ann_commented.runWithDL3(G_copy, D_copy, th)
      
#         # Check if division of labor was achieved
#         if result[-1] == 0:  # Division of labor was achieved
#             print("achieve DOL")
#             solution_counts += 1
#     return solution_counts

# # Run the count_solutions function multiple times with the same G and D
# num_trials = 10000
# solution_counts = count_solutions(G, D, num_trials)
# print(solution_counts)




##################################################################################################################################

# import divisionGame_ann_commented
# import networkx as nx
# import random
# import numpy as np
# import csv
# import numOfSolutionsDepthC
# import divisionGame

# ofile = csv.writer(open("../../data/data_pref_attach_2_without_storage_item3.csv", "w"))
# # ofile = csv.writer(open("../../data/data_pref_attach_2_without_storage_item2.csv", "w"))
# # ofile = csv.writer(open("../../data/data_pref_attach_2_without_storage_item4.csv", "w"))
# # ofile = csv.writer(open("../../data/data_pref_attach_2_with_storage_item3.csv", "w"))
# ofile.writerows([["gameId", "size", "#solutions", "ave_rate", "sd_rate"]])

# n = 20 # nunber of nodes
# th = 0 # 100000 # threshold that represents storage capacity

# for k in range(1):
#     print(k)
#     # Generate a network from the edgelists
#     filename = '../../data/networks/pa_2/pa_2_2_' + str(k) + '.edgelist'
#     dataFile = csv.reader(open(filename, 'r'))

#     G = nx.Graph()
#     for data in dataFile:
#         data = list(map(lambda x:x.strip(), data))
#         data2 = data[0].split(" ")
#         u1 = int(data2[0])
#         u2 = int(data2[1])
#         G.add_edge(u1, u2)

#     cp = numOfSolutionsDepthC.getNumOfSolutions(G) # calculate solution number with chromatic number
#     # cluster = nx.average_clustering(G) # calculate clustering coeff
#     # path = nx.average_shortest_path_length(G) # calculate average shortest path length

#     Rate = []
#     for j in range (100):

#         D = {}
#         for gn in list(G.nodes()):
#             D[gn] = 0

#         # Initialize node color for 3 items
#         # 0 = generalization, 1 = specialization of item1, 2 = specialization of item2, 3 = specialization of item3
#         cycls_3 = [c for c in nx.cycle_basis(G) if len(c)==3]
#         e = random.choice(cycls_3)
#         D[e[0]] = 1
#         D[e[1]] = 2
#         D[e[2]] = 3

#         # Initialize node color for 2 items
#         # e = random.choice(list(G.edges()))
#         # D[e[0]] = 1
#         # D[e[1]] = 2

#         # Initialize node color for 4 items
#         # cycls_3 = [c for c in nx.cycle_basis(G) if len(c)==3]
#         # e = random.choice(cycls_3)
#         # D[e[0]] = 1
#         # D[e[1]] = 2
#         # D[e[2]] = 3
#         # max_v = 0
#         # max_gn = None
#         # for gn in G.nodes():
#         #    if gn not in e:
#         #        vv = 0
#         #        for en in e:
#         #            if G.has_edge(gn, en):
#         #                vv += 1
#         #        if vv > max_v:
#         #            max_v = vv
#         #            max_gn = gn
#         # D[max_gn] = 4

#         # Run the simulation
#         rate = divisionGame.runWithDL3(G, D, th) # Division of labor game with 3 items
#         # rate = divisionGame.runWithDL2(G, D, th) # Division of labor game with 2 items
#         # rate = divisionGame.runWithDL4(G, D, th) # Division of labor game with 4 items

#         Rate.append(1.0 * rate[-1] / n)

#     # Record the data
#     ofile.writerows([[k, n, cp, np.mean(Rate), np.std(Rate)]])

# # def count_solutions(num_trials):
# #     solution_counts = {}

# #     for _ in range(num_trials):
# #         # result = divisionGame_ann_commented._runWithDL3(Nodes, Neighbors, C, A, h)
# #         result = divisionGame_ann_commented.runWithDL3(G, D, th)
      
# #         #Check if division of labor was achieved
# #         if result[-1] == 0:  # Division of labor was achieved
            
# #             solution = tuple(C)  # Snapshot of the current solution

# #             if solution in solution_counts:
# #                 solution_counts[solution] += 1
# #             else:
# #                 solution_counts[solution] = 1

# #     return solution_counts

# def count_solutions(num_trials):
#     solution_counts = 0

#     for _ in range(num_trials):
#         # result = divisionGame_ann_commented._runWithDL3(Nodes, Neighbors, C, A, h)
#         result = divisionGame_ann_commented.runWithDL3(G, D, th)
      
#         #Check if division of labor was achieved
#         if result[-1] == 0:  # Division of labor was achieved
#             print("achieve DOL")
#             solution_counts += 1
 

#     return solution_counts

# # you can now use the functions from the division_labor module
# num_trials = 10000
# solution_counts = count_solutions(num_trials)
# print(solution_counts)



# The code that generates completion rate (first version)
##################################################################################################################################


# import copy
# import divisionGame_ann_commented
# import networkx as nx
# import random
# import numpy as np
# import csv
# import numOfSolutionsDepthC
# import divisionGame

# ofile = csv.writer(open("../../data/data_pref_attach_2_without_storage_item3.csv", "w"))
# ofile.writerows([["gameId", "size", "#solutions", "ave_rate", "sd_rate"]])

# n = 3 # number of nodes
# th = 0 # threshold that represents storage capacity

# def count_solutions(G, D, num_trials):
#     solution_counts = 0
#     for _ in range(num_trials):
#         G_copy = copy.deepcopy(G)
#         D_copy = copy.deepcopy(D)
#         result = divisionGame_ann_commented.runWithDL3(G_copy, D_copy, th)
      
#         # Check if division of labor was achieved
#         if result[-1] == 0:  # Division of labor was achieved
#             print("achieve DOL")
#             solution_counts += 1
#     return solution_counts

# def calculate_node_completion_rate(G, D, num_trials):
#     total_nodes = len(G.nodes())
#     total_colors = set(D.values())  # total distinct colors in the graph
#     node_wins = 0

#     for _ in range(num_trials):
#         G_copy = copy.deepcopy(G)
#         D_copy = copy.deepcopy(D)
#         divisionGame_ann_commented.runWithDL3(G_copy, D_copy, th)

#         for node in D_copy:
#             neighbor_colors = set(D_copy[neighbor] for neighbor in G_copy.neighbors(node))

#             # Increment node wins if the neighbors collectively possess all colors
#             if total_colors.issubset(neighbor_colors):
#                 node_wins += 1

#     # Calculate and return the completion rate
#     return node_wins / (total_nodes * num_trials)

# for k in range(500):
#     print(k)
#     filename = '../../data/networks/pa_2/pa_2_2_' + str(k) + '.edgelist'
#     dataFile = csv.reader(open(filename, 'r'))

#     G = nx.Graph()
#     for data in dataFile:
#         data = list(map(lambda x:x.strip(), data))
#         data2 = data[0].split(" ")
#         u1 = int(data2[0])
#         u2 = int(data2[1])
#         G.add_edge(u1, u2)

#     D = {}
#     for gn in list(G.nodes()):
#         D[gn] = 0

#     # Initialize node color for 3 items
#     cycls_3 = [c for c in nx.cycle_basis(G) if len(c)==3]
#     e = random.choice(cycls_3)
#     D[e[0]] = 1
#     D[e[1]] = 2
#     D[e[2]] = 3

#     # Run the count_solutions function multiple times with the same G and D
#     num_trials = 100
#     # solution_counts = count_solutions(G, D, num_trials)
#     # print("solution counts:", solution_counts)

#     node_completion_rate = calculate_node_completion_rate(G, D, num_trials)
#     print("Node completion rate:", node_completion_rate)

# NetworkX's Barabási–Albert graph generator
# The issue is that both the Barabasi-Albert and Watts-Strogatz models do not 
# guarantee cycles of length 3, which are required by our current color 
# initialization logic.
##################################################################################################################################

# import copy
# import divisionGame_ann_commented
# import networkx as nx
# import random
# import numpy as np
# import csv
# import numOfSolutionsDepthC
# import divisionGame

# ofile = csv.writer(open("../../data/data_pref_attach_2_without_storage_item3.csv", "w"))
# ofile.writerows([["gameId", "size", "#solutions", "ave_rate", "sd_rate"]])

# n = 4  # number of nodes
# m = 3  # number of edges to attach from a new node to existing nodes
# th = 0  # threshold that represents storage capacity

# for k in range(500):
#     print(k)
    
#     # Generate a Barabási–Albert graph instead of reading from an .edgelist file
#     G = nx.barabasi_albert_graph(n, m)

#     D = {}
#     for gn in list(G.nodes()):
#         D[gn] = 0

#     # Initialize node color for 3 items
#     cycls_3 = [c for c in nx.cycle_basis(G) if len(c)==3]
#     if not cycls_3:
#         continue
#     e = random.choice(cycls_3)
#     D[e[0]] = 1
#     D[e[1]] = 2
#     D[e[2]] = 3

#     # Run the count_solutions function multiple times with the same G and D
#     num_trials = 100

#     node_completion_rate = calculate_node_completion_rate(G, D, num_trials)
#     print("Node completion rate:", node_completion_rate)

##################################################################################################################################
# use a different model that should create more cycles. 
# The nx.newman_watts_strogatz_graph function should do a better job at this, 
# as it doesn't rewire edges but instead adds new edges with a probability p. 
# This should increase the chance of cycles of length 3.

# import copy
# import divisionGame_ann_commented
# import networkx as nx
# import random
# import numpy as np
# import csv
# import numOfSolutionsDepthC
# import divisionGame

# ofile = csv.writer(open("../../data/data_pref_attach_2_without_storage_item3.csv", "w"))
# ofile.writerows([["gameId", "size", "#solutions", "ave_rate", "sd_rate"]])

# n = 20  # number of nodes
# k = 4  # each node is connected to k nearest neighbors in ring topology
# p = 0.5  # the probability of adding a new edge for each edge
# th = 0  # threshold that represents storage capacity


# def calculate_node_completion_rate(G, D, num_trials):
#     total_nodes = len(G.nodes())
#     total_colors = set(D.values())  # total distinct colors in the graph
#     node_wins = 0

#     for _ in range(num_trials):
#         G_copy = copy.deepcopy(G)
#         D_copy = copy.deepcopy(D)
#         divisionGame_ann_commented.runWithDL3(G_copy, D_copy, th)

#         for node in D_copy:
#             neighbor_colors = set(D_copy[neighbor] for neighbor in G_copy.neighbors(node))

#             # Increment node wins if the neighbors collectively possess all colors
#             if total_colors.issubset(neighbor_colors):
#                 node_wins += 1

#     # Calculate and return the completion rate
#     return node_wins / (total_nodes * num_trials)
# for i in range(500):
#     print(i)
    
#     # Generate a Newman-Watts-Strogatz graph instead of reading from an .edgelist file
#     G = nx.newman_watts_strogatz_graph(n, k, p)

#     D = {}
#     for gn in list(G.nodes()):
#         D[gn] = 0

#     # Initialize node color for 3 items
#     cycls_3 = [c for c in nx.cycle_basis(G) if len(c)==3]
#     if not cycls_3:
#         continue
#     e = random.choice(cycls_3)
#     D[e[0]] = 1
#     D[e[1]] = 2
#     D[e[2]] = 3

#     # Run the count_solutions function multiple times with the same G and D
#     num_trials = 100

#     node_completion_rate = calculate_node_completion_rate(G, D, num_trials)
#     print("Node completion rate:", node_completion_rate)

##################################################################################################################################
# Sherrie's graph generator function

# import copy
# import divisionGame_ann_commented
# import networkx as nx
# import random
# import numpy as np
# import csv
# import numOfSolutionsDepthC
# import divisionGame
# import os

# th = 0

# def calculate_node_completion_rate(G, D, num_trials):
#     total_nodes = len(G.nodes())
#     total_colors = set(D.values())  # total distinct colors in the graph
#     node_wins = 0

#     for _ in range(num_trials):
#         G_copy = copy.deepcopy(G)
#         D_copy = copy.deepcopy(D)
#         divisionGame_ann_commented.runWithDL3(G_copy, D_copy, th)

#         for node in D_copy:
#             neighbor_colors = set(D_copy[neighbor] for neighbor in G_copy.neighbors(node))

#             # Increment node wins if the neighbors collectively possess all colors
#             if total_colors.issubset(neighbor_colors):
#                 node_wins += 1

#     # Calculate and return the completion rate
#     return node_wins / (total_nodes * num_trials)

# directory = "../../data/networks/random_10/"
# for filename in os.listdir(directory):
#     if filename.endswith(".edgelist"):
#         print(filename)
        
#         G = nx.read_edgelist(os.path.join(directory, filename))

#         D = {}
#         for gn in list(G.nodes()):
#             D[gn] = 0

#         # Initialize node color for 3 items
#         cycls_3 = [c for c in nx.cycle_basis(G) if len(c)==3]
#         if not cycls_3:
#             continue
#         e = random.choice(cycls_3)
#         D[e[0]] = 1
#         D[e[1]] = 2
#         D[e[2]] = 3

#         # Run the count_solutions function multiple times with the same G and D
#         num_trials = 100

#         node_completion_rate = calculate_node_completion_rate(G, D, num_trials)
#         print("Node completion rate:", node_completion_rate)



##################################################################################################################################

import os
import copy
import divisionGame_ann_commented
import networkx as nx
import random
import numpy as np
import csv
import numOfSolutionsDepthC
import divisionGame

directory = "../../data/networks/random_10/"

th = 0

# def calculate_node_completion_rate(G, D, num_trials):
#     total_nodes = len(G.nodes())
#     total_colors = set(D.values())  # total distinct colors in the graph
#     node_wins = 0

#     for _ in range(num_trials):
#         divisionGame_ann_commented.runWithDL3(G, D, th)

#         for node in D:
#             neighbor_colors = set(D[neighbor] for neighbor in G.neighbors(node))

#             # Increment node wins if the neighbors collectively possess all colors
#             if total_colors.issubset(neighbor_colors):
#                 node_wins += 1

#     # Calculate and return the completion rate
#     return node_wins / (total_nodes * num_trials)


# def calculate_node_completion_rate(G, D, num_trials):
#     total_nodes = len(G.nodes())
#     node_wins = 0

#     for _ in range(num_trials):
#         divisionGame_ann_commented.runWithDL3(G, D, th)

#         for node in D:
#             neighbor_colors = set(D[neighbor] for neighbor in G.neighbors(node))

#             # Increment node wins if the neighbors collectively possess all colors
#             if total_colors.issubset(neighbor_colors):
#                 node_wins += 1

#     # Calculate and return the completion rate
#     return node_wins / (total_nodes * num_trials)


def calculate_node_completion_rate(G, D, num_trials):
    total_nodes = len(G.nodes())
    Rate = []
    for _ in range (num_trials):
        
        rate = divisionGame_ann_commented.runWithDL3(G, D, th)
        Rate.append(1.0 * rate[-1] / total_nodes)
    return 1- np.mean(Rate)
    # total_nodes = len(G.nodes())
    # node_fails = 0

    # for _ in range(num_trials):
    #     R = divisionGame_ann_commented.runWithDL3(G, D, th)
    #     # total = np.sum(R)
    #     node_fails += R[-1]
    
    # return (1- (node_fails / (total_nodes * num_trials)))


for filename in os.listdir(directory):
    if filename.endswith(".edgelist"):
        print(filename)
        
        G = nx.read_edgelist(os.path.join(directory, filename), nodetype=int)

        D = {}
        for gn in list(G.nodes()):
            D[gn] = 0

        # # Initialize node color for 3 items
        # cycls_3 = [c for c in nx.cycle_basis(G) if len(c)==3]
        # if not cycls_3:
        #     continue
        # e = random.choice(cycls_3)
        # D[e[0]] = 1
        # D[e[1]] = 2
        # D[e[2]] = 3

        # Initialize node color for 3 items
        cycls_3 = [c for c in nx.cycle_basis(G) if len(c)==3]
        if not cycls_3:
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

        # Run the count_solutions function multiple times with the same G and D
        num_trials = 100

        node_completion_rate = calculate_node_completion_rate(G, D, num_trials)
        print("Node completion rate:", node_completion_rate)

