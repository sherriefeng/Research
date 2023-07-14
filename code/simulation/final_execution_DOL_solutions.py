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




##################################################################################################################################


import copy
import divisionGame_ann_commented
import networkx as nx
import random
import numpy as np
import csv
import numOfSolutionsDepthC
import divisionGame

ofile = csv.writer(open("../../data/data_pref_attach_2_without_storage_item3.csv", "w"))
ofile.writerows([["gameId", "size", "#solutions", "ave_rate", "sd_rate"]])

n = 20 # number of nodes
th = 0 # threshold that represents storage capacity

def count_solutions(G, D, num_trials):
    solution_counts = 0
    for _ in range(num_trials):
        G_copy = copy.deepcopy(G)
        D_copy = copy.deepcopy(D)
        result = divisionGame_ann_commented.runWithDL3(G_copy, D_copy, th)
      
        # Check if division of labor was achieved
        if result[-1] == 0:  # Division of labor was achieved
            print("achieve DOL")
            solution_counts += 1
    return solution_counts

for k in range(500):
    print(k)
    filename = '../../data/networks/pa_2/pa_2_2_' + str(k) + '.edgelist'
    dataFile = csv.reader(open(filename, 'r'))

    G = nx.Graph()
    for data in dataFile:
        data = list(map(lambda x:x.strip(), data))
        data2 = data[0].split(" ")
        u1 = int(data2[0])
        u2 = int(data2[1])
        G.add_edge(u1, u2)

    D = {}
    for gn in list(G.nodes()):
        D[gn] = 0

    # Initialize node color for 3 items
    cycls_3 = [c for c in nx.cycle_basis(G) if len(c)==3]
    e = random.choice(cycls_3)
    D[e[0]] = 1
    D[e[1]] = 2
    D[e[2]] = 3

    # Run the count_solutions function multiple times with the same G and D
    num_trials = 100
    solution_counts = count_solutions(G, D, num_trials)
    print("solution counts:", solution_counts)

