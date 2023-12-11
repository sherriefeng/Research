import numpy as np
cimport numpy as np

import os
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
import uuid
import time

DTYPE = np.int64
ctypedef np.int64_t DTYPE_t


def save_init_final_fig(Nodes, Neighbors, C, initial_node_colors):
    G = nx.Graph()
    G.add_nodes_from(Nodes)
    for node, neighbors in Neighbors.items():
        G.add_edges_from((node, neighbor) for neighbor in neighbors)

    frame_dir = "figures"
    os.makedirs(frame_dir, exist_ok=True)
    
    # Save final config
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G, seed = 100)
    final_node_colors = [C[node] for node in Nodes]
    nx.draw(G, pos, node_color=final_node_colors, cmap=matplotlib.colormaps.get_cmap('cool'), with_labels=True)
    unique_filename = f'final_{str(uuid.uuid4())}.png'
    frame_path = os.path.join(frame_dir, unique_filename)
    plt.savefig(frame_path)
    plt.close()

    # Save initial config
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G, seed = 100)
    nx.draw(G, pos, node_color=initial_node_colors, cmap=matplotlib.colormaps.get_cmap('cool'), with_labels=True)
    unique_filename = f'init_{str(uuid.uuid4())}.png'
    frame_path = os.path.join(frame_dir, unique_filename)
    plt.savefig(frame_path)
    plt.close()


#########
# Division of labor game with 3 items, trying to optimize
#########

cdef tuple _runWithDL3_mod(list Nodes, dict Neighbors, np.ndarray[DTYPE_t, ndim=1] C, np.ndarray[DTYPE_t, ndim=1] A, dict h):
    cdef int nsize = len(Nodes)
    cdef int n, neighbor, learner, k, nei
    cdef int is1, is2, is3
    cdef int numD = 0
    cdef int isDef = 1
    cdef int numSim = 1000 # 5000
    
    cdef np.ndarray[DTYPE_t, ndim=1] R = np.zeros(numSim, dtype=DTYPE) # Rate of incompletion for each simulation
    cdef np.ndarray[DTYPE_t, ndim=1] neighborhood_missing_colors = np.zeros(nsize, dtype=DTYPE) # neighborhood completeness

    # New: Initialize color counts for each node and its neighbors
    cdef dict node_color_counts = {node: {1: 0, 2: 0, 3: 0} for node in Nodes}
    cdef dict num_satisfied = {node: 0 for node in Nodes}
    cdef dict thresholds = h # {node: h[node] * 100 for node in Nodes}

    for i in range(numSim):
        learner = np.random.choice(Nodes)
        threshold = thresholds[learner]
        neighbors_colors = np.array([C[neighbor] for neighbor in Neighbors[learner]], dtype=DTYPE)
        
        is1, is2, is3 = np.isin([1, 2, 3], neighbors_colors)

        # If division of labor is solved in the node's neighborhood
        if is1 == 1 and is2 == 1 and is3 == 1:
            if A[learner] < threshold:
                C[learner] = np.random.choice([1, 2, 3])
                A[learner] += 1
            else:
                # Update: Reset color counts for the learner and its neighbors
                C[learner] = 0
                A[learner] = 0
        
        elif is1 == 1 and is2 == 1 and is3 == 0:
            C[learner] = 3
            A[learner] = 0

        elif is1 == 0 and is2 == 1 and is3 == 1:
            C[learner] = 1
            A[learner] = 0

        elif is1 == 1 and is2 == 0 and is3 == 1:
            C[learner] = 2
            A[learner] = 0

        else:
            if A[learner] < threshold:
                if is1 == 1:
                    C[learner] = np.random.choice([2, 3])
                elif is2 == 1:
                    C[learner] = np.random.choice([1, 3])
                elif is3 == 1:
                    C[learner] = np.random.choice([1, 2])
                else:
                    if C[learner] == 0:
                        C[learner] = np.random.choice([1, 2, 3])
                A[learner] += 1
            else:
                C[learner] = 0
                A[learner] = 0
        
        # Update node_color_counts after node change
        for color in [1, 2, 3]:
            node_color_counts[learner][color] = np.sum(neighbors_colors + [C[learner]] == color)
            num_satisfied[learner] = sum(count > 0 for count in node_color_counts[learner].values())

            for nei in Neighbors[learner]:
                node_color_counts[nei][color] = np.sum(np.array([C[node] for node in Neighbors[nei]] + [C[nei]], dtype=DTYPE) == color)
                num_satisfied[nei] = sum(count > 0 for count in node_color_counts[nei].values())

    numD = 0
    # Count the number of nodes that have not satisfied DoL
    for k in range(nsize):
        if num_satisfied[k] < 3:
            numD += 1
        neighborhood_missing_colors[k] = 3 - num_satisfied[k]

    R[i] = numD # Number of incomplete nodes
    
    return R, neighborhood_missing_colors


def runWithDL3_mod(G, CD, h):
    # Initializes A (how many times the node has solved DoL, contingent on threshold) as zero arrays
    cdef np.ndarray[DTYPE_t, ndim=1] C = np.zeros(len(G.nodes()), dtype=DTYPE)
    cdef np.ndarray[DTYPE_t, ndim=1] A = np.zeros(len(G.nodes()), dtype=DTYPE)
    cdef dict Neighbors = {}
    cdef dict h2 = h # Threshold

    # Initializes C (specialization of each node), same as D in run files
    for n in G.nodes():
        C[n] = CD[n]
        Neighbors[n] = list(G.neighbors(n))

    cdef list Nodes = list(G.nodes())

    R, neighborhood_missing_colors = _runWithDL3_mod(Nodes, Neighbors, C, A, h2)

    # Return both the neighborhood completeness metric at the end and the original incompletion rate
    return R, neighborhood_missing_colors


#########
# Division of labor game with 3 items, no movie
#########

cdef tuple _runWithDL3_het(list Nodes, dict Neighbors, np.ndarray[DTYPE_t, ndim=1] C, np.ndarray[DTYPE_t, ndim=1] A, dict h):
    cdef int nsize = len(Nodes)
    cdef int n, neighbor, learner, k, nei
    cdef int is1, is2, is3
    cdef int numD = 0
    cdef int isDef = 1
    cdef int numSim = 5000
    cdef np.ndarray[DTYPE_t, ndim=1] R = np.zeros(numSim, dtype=DTYPE) # Rate of incompletion for each simulation

    cdef np.ndarray[DTYPE_t, ndim=1] neighborhood_metrics = np.zeros(nsize, dtype=DTYPE) # neighborhood completeness
    cdef np.ndarray[DTYPE_t, ndim=1] neighborhood_missing_colors = np.zeros(nsize, dtype=DTYPE) # neighborhood completeness

    for i in range(numSim):
        learner = np.random.choice(Nodes)
        threshold = h[learner] * 100
        neighbors_colors = np.array([C[neighbor] for neighbor in Neighbors[learner]], dtype=DTYPE)
        is1, is2, is3 = np.isin([1, 2, 3], neighbors_colors)

        # is1 = 0
        # is2 = 0
        # is3 = 0

        # Updates neighbor specialization booleans
        # for neighbor in Neighbors[learner]:
        #    if C[neighbor] == 1:
        #        is1 = 1
        #    elif C[neighbor] == 2:
        #        is2 = 1
        #    elif C[neighbor] == 3:
        #        is3 = 1

        # If division of labor is solved in the node's neighborhood
        if is1 == 1 and is2 == 1 and is3 == 1:
            # If threshold is not passed, randomly assign new specialization to node
            if A[learner] < threshold:
                # if C[learner] == 0:
                C[learner] = np.random.choice([1, 2, 3])
                A[learner] += 1
            else:
                C[learner] = 0
                A[learner] = 0
        
        elif is1 == 1 and is2 == 1 and is3 == 0:
            C[learner] = 3
            A[learner] = 0

        elif is1 == 0 and is2 == 1 and is3 == 1:
            C[learner] = 1
            A[learner] = 0

        elif is1 == 1 and is2 == 0 and is3 == 1:
            C[learner] = 2
            A[learner] = 0

        else:
            if A[learner] < threshold:
                if is1 == 1:
                    C[learner] = np.random.choice([2, 3])
                elif is2 == 1:
                    C[learner] = np.random.choice([1, 3])
                elif is3 == 1:
                    C[learner] = np.random.choice([1, 2])
                else:
                    if C[learner] == 0:
                        C[learner] = np.random.choice([1, 2, 3])
                A[learner] += 1
            else:
                C[learner] = 0
                A[learner] = 0


        numD = 0 # Number of nodes that have not satisfied DoL
        for k in range(nsize):
            is1 = 0
            is2 = 0
            is3 = 0
            if C[k] == 1:
                is1 = 1
            elif C[k] == 2:
                is2 = 1
            elif C[k] == 3:
                is3 = 1
            for neighbor in Neighbors[k]:
                if C[neighbor] == 1:
                    is1 = 1
                elif C[neighbor] == 2:
                    is2 = 1
                elif C[neighbor] == 3:
                    is3 = 1
            if is1 == 0 or is2 == 0 or is3 == 0:
                numD += 1

        R[i] = numD # Number of incomplete nodes
        if numD == 0:
            break;
    
    # Calculate the neighborhood completeness metric for each neighborhood at the end
    for k in range(nsize):
        numD = 0
        is1 = 0
        is2 = 0
        is3 = 0
        if C[k] == 1:
            is1 = 1
        elif C[k] == 2:
            is2 = 1
        elif C[k] == 3:
            is3 = 1
        for neighbor in Neighbors[k]:
            if C[neighbor] == 1:
                is1 = 1
            elif C[neighbor] == 2:
                is2 = 1
            elif C[neighbor] == 3:
                is3 = 1
        if is1 == 0 or is2 == 0 or is3 == 0:
            numD += 1

        # Calculate neighborhood completeness metric for the current node's neighborhood
        # completeness = 1 - (numD / len(Neighbors[k]))
        # neighborhood_metrics[k] = completeness

        # Calculate the count of missing colors in the neighborhood
        missing_colors = 3 - (is1 + is2 + is3)
        neighborhood_missing_colors[k] = missing_colors
    
    #print(neighborhood_missing_colors)
    #neighborhood_metrics = neighborhood_missing_colors / 3.0

    # Calculate the weighted sum of neighborhood completeness
    #print(neighborhood_metrics)
    #weighted_avg = np.sum(neighborhood_metrics)
    
    return R, neighborhood_missing_colors

def runWithDL3_het(G, CD, h):
    # Initializes A (how many times the node has solved DoL, contingent on threshold) as zero arrays
    cdef np.ndarray[DTYPE_t, ndim=1] C = np.zeros(len(G.nodes()), dtype=DTYPE)
    cdef np.ndarray[DTYPE_t, ndim=1] A = np.zeros(len(G.nodes()), dtype=DTYPE)
    cdef dict Neighbors = {}
    cdef dict h2 = h # Threshold

    # Initializes C (specialization of each node), same as D in run files
    for n in G.nodes():
        C[n] = CD[n]
        Neighbors[n] = list(G.neighbors(n))

    cdef list Nodes = list(G.nodes())

    # return _runWithDL3_het(Nodes, Neighbors, C, A, h2) # Returns # of incompleted nodes

    R, neighborhood_missing_colors = _runWithDL3_het(Nodes, Neighbors, C, A, h2)

    # Return both the neighborhood completeness metric at the end and the original incompletion rate
    return R, neighborhood_missing_colors


#########
# Division of labor game with 3 items, no movie, modified to not default to generalization
#########

cdef tuple _runWithDL3_nogen(list Nodes, dict Neighbors, np.ndarray[DTYPE_t, ndim=1] C, np.ndarray[DTYPE_t, ndim=1] A, int h):
    cdef int nsize = len(Nodes)
    cdef int n, neighbor, learner, k, nei
    cdef int is1, is2, is3
    cdef int numD = 0
    cdef int numE = 0       # Added variable, number of nodes that are not colored
    cdef int isDef = 1
    cdef int numSim = 5000   # Modified value
    cdef np.ndarray[DTYPE_t, ndim=1] R = np.zeros(numSim, dtype=DTYPE) # Rate of incompletion for each simulation

    initial_node_colors = [C[node] for node in Nodes]

    for i in range(numSim):
        learner = np.random.choice(Nodes)
        is1 = 0
        is2 = 0
        is3 = 0

        # Updates neighbor specialization booleans
        # DOES NOT INCLUDE THE NODE'S OWN COLOR!
        for neighbor in Neighbors[learner]:
            # print("Neighbor:", neighbor, "Color:", C[neighbor])
            if C[neighbor] == 1:
                is1 = 1
            elif C[neighbor] == 2:
                is2 = 1
            elif C[neighbor] == 3:
                is3 = 1
        
        # print("Node:", learner, "Neighbors:", Neighbors[learner], "Status:", is1, is2, is3)

        # If division of labor is solved in the node's neighborhood
        if is1 == 1 and is2 == 1 and is3 == 1:
            # If threshold is not passed, randomly assign new specialization to node
            if A[learner] < h:
                # if C[learner] == 0:
                C[learner] = np.random.choice([1, 2, 3]) # This is not greedy?
                A[learner] += 1
            
            # print("Satisfies DoL!")
            #else:
            #    # Default to generalization?
            #    C[learner] = 0
            #    A[learner] = 0
        
        elif is1 == 1 and is2 == 1 and is3 == 0:
            C[learner] = 3
            A[learner] = 0

            is3 == 1 # Updated to reflect completion

        elif is1 == 0 and is2 == 1 and is3 == 1:
            C[learner] = 1
            A[learner] = 0

            is1 == 1 # Updated to reflect completion

        elif is1 == 1 and is2 == 0 and is3 == 1:
            C[learner] = 2
            A[learner] = 0

            is2 == 1 # Updated to reflect completion

        else:
            if A[learner] < h:
                if is1 == 1:
                    C[learner] = np.random.choice([2, 3])
                elif is2 == 1:
                    C[learner] = np.random.choice([1, 3])
                elif is3 == 1:
                    C[learner] = np.random.choice([1, 2])
                else:
                    if C[learner] == 0:
                        C[learner] = np.random.choice([1, 2, 3])
                A[learner] += 1
            else:
                # Default to generalization, not enough incentive
                # print("Defaulting Node:", learner, "Neighbors:", Neighbors[learner], "Status:", is1, is2, is3)
                C[learner] = 0
                A[learner] = 0

        numD = 0 # Number of nodes that have not satisfied DoL
        numE = 0 # Number of nodes that are not colored
        for k in range(nsize):
            is1 = 0
            is2 = 0
            is3 = 0
            if C[k] == 1:
                is1 = 1
            elif C[k] == 2:
                is2 = 1
            elif C[k] == 3:
                is3 = 1
            for neighbor in Neighbors[k]:
                if C[neighbor] == 1:
                    is1 = 1
                elif C[neighbor] == 2:
                    is2 = 1
                elif C[neighbor] == 3:
                    is3 = 1
            if is1 == 0 or is2 == 0 or is3 == 0:
                numD += 1

            if is1 == 0 and is2 == 0 and is3 == 0:
                numE += 1

        R[i] = numD # Number of incomplete nodes
        if numD == 0:
            break;

        # # Exit if no nodes are colored
        # if numE == nsize:
        #    print("Exiting on no colored nodes")
        #    return R;

    return R, i

def runWithDL3_nogen(G, CD, h):
    # Initializes C and A (how many times the node has solved DoL, contingent on threshold) as zero arrays
    cdef np.ndarray[DTYPE_t, ndim=1] C = np.zeros(len(G.nodes()), dtype=DTYPE)
    cdef np.ndarray[DTYPE_t, ndim=1] A = np.zeros(len(G.nodes()), dtype=DTYPE)
    cdef dict Neighbors = {}
    cdef int h2 = h # Threshold

    for n in G.nodes():
        C[n] = CD[n]
        Neighbors[n] = list(G.neighbors(n))

    cdef list Nodes = list(G.nodes())

    return _runWithDL3_nogen(Nodes, Neighbors, C, A, h2) # Returns # of incompleted nodes


#########
# Division of labor game with 3 items, with movie
#########

cdef np.ndarray[DTYPE_t, ndim=1] _runWithDL3_movie(list Nodes, dict Neighbors, np.ndarray[DTYPE_t, ndim=1] C, np.ndarray[DTYPE_t, ndim=1] A, int h):
    cdef int nsize = len(Nodes)
    cdef int n, neighbor, learner, k, nei
    cdef int is1, is2, is3
    cdef int numD = 0
    cdef int numE = 0       # Added variable, number of nodes that are not colored
    cdef int isDef = 1
    cdef int numSim = 1000   # Modified value
    cdef np.ndarray[DTYPE_t, ndim=1] R = np.zeros(numSim, dtype=DTYPE) # Rate of incompletion for each simulation

    frame_dir = "movie"

    # Initialize a graph
    G = nx.Graph()
    G.add_nodes_from(Nodes)
    for node, neighbors in Neighbors.items():
        G.add_edges_from((node, neighbor) for neighbor in neighbors)

    for i in range(numSim):
        learner = np.random.choice(Nodes)
        is1 = 0
        is2 = 0
        is3 = 0

        # Updates neighbor specialization booleans
        # DOES NOT INCLUDE THE NODE'S OWN COLOR!
        for neighbor in Neighbors[learner]:
            # print("Neighbor:", neighbor, "Color:", C[neighbor])
            if C[neighbor] == 1:
                is1 = 1
            elif C[neighbor] == 2:
                is2 = 1
            elif C[neighbor] == 3:
                is3 = 1
        
        # print("Node:", learner, "Neighbors:", Neighbors[learner], "Status:", is1, is2, is3)

        # If division of labor is solved in the node's neighborhood
        if is1 == 1 and is2 == 1 and is3 == 1:
            # If threshold is not passed, randomly assign new specialization to node
            if A[learner] < h:
                # if C[learner] == 0:
                C[learner] = np.random.choice([1, 2, 3]) # This is not greedy?
                A[learner] += 1
            
            # print("Satisfies DoL!")
            #else:
            #    # Default to generalization?
            #    C[learner] = 0
            #    A[learner] = 0
        
        elif is1 == 1 and is2 == 1 and is3 == 0:
            C[learner] = 3
            A[learner] = 0

            is3 == 1

        elif is1 == 0 and is2 == 1 and is3 == 1:
            C[learner] = 1
            A[learner] = 0

            is1 == 1

        elif is1 == 1 and is2 == 0 and is3 == 1:
            C[learner] = 2
            A[learner] = 0

            is2 == 1

        else:
            if A[learner] < h:
                if is1 == 1:
                    C[learner] = np.random.choice([2, 3])
                elif is2 == 1:
                    C[learner] = np.random.choice([1, 3])
                elif is3 == 1:
                    C[learner] = np.random.choice([1, 2])
                else:
                    if C[learner] == 0:
                        C[learner] = np.random.choice([1, 2, 3])
                A[learner] += 1
            else:
                # Default to generalization
                # print("Defaulting Node:", learner, "Neighbors:", Neighbors[learner], "Status:", is1, is2, is3)
                C[learner] = 0
                A[learner] = 0
            
        # Capture graph visualization
        print(i)

        plt.figure(figsize=(8, 6))
        pos = nx.spring_layout(G, seed = 100)
        node_colors = [C[node] for node in Nodes]
        nx.draw(G, pos, node_color=node_colors, cmap=matplotlib.colormaps.get_cmap('cool'), with_labels=True)

        # Save the frame to the specified directory
        frame_path = os.path.join(frame_dir, f'frame_{i:04d}.png')
        plt.savefig(frame_path)
        plt.close()

        numD = 0 # Number of nodes that have not satisfied DoL
        numE = 0 # Number of nodes that are not colored
        for k in range(nsize):
            is1 = 0
            is2 = 0
            is3 = 0
            if C[k] == 1:
                is1 = 1
            elif C[k] == 2:
                is2 = 1
            elif C[k] == 3:
                is3 = 1
            for neighbor in Neighbors[k]:
                if C[neighbor] == 1:
                    is1 = 1
                elif C[neighbor] == 2:
                    is2 = 1
                elif C[neighbor] == 3:
                    is3 = 1
            if is1 == 0 or is2 == 0 or is3 == 0:
                numD += 1

            if is1 == 0 and is2 == 0 and is3 == 0:
                numE += 1

        R[i] = numD # Number of incomplete nodes
        if numD == 0:
            break;

        # Exit if no nodes are colored
        # if numE == nsize:
        #    print("Exiting on no colored nodes")
        #    return R;

    return R

def runWithDL3_movie(G, CD, h):
    # Initializes C and A (how many times the node has solved DoL, contingent on threshold) as zero arrays
    cdef np.ndarray[DTYPE_t, ndim=1] C = np.zeros(len(G.nodes()), dtype=DTYPE)
    cdef np.ndarray[DTYPE_t, ndim=1] A = np.zeros(len(G.nodes()), dtype=DTYPE)
    cdef dict Neighbors = {}
    cdef int h2 = h # Threshold

    # Populates C (specialization of each node), same as D in run files
    # C = np.array([np.int64(CD.get(node, 0)) for node in G.nodes()])
    # print([(node, color) for node, color in enumerate(C)])

    for n in G.nodes():
        C[n] = CD[n]
        Neighbors[n] = list(G.neighbors(n))

    print([(node, color) for node, color in enumerate(C)])

    cdef list Nodes = list(G.nodes())

    return _runWithDL3_movie(Nodes, Neighbors, C, A, h2) # Returns # of incompleted nodes



#########
# Division of labor game with 3 items, no movie
#########

cdef np.ndarray[DTYPE_t, ndim=1] _runWithDL3(list Nodes, dict Neighbors, np.ndarray[DTYPE_t, ndim=1] C, np.ndarray[DTYPE_t, ndim=1] A, int h):
    cdef int nsize = len(Nodes)
    cdef int n, neighbor, learner, k, nei
    cdef int is1, is2, is3
    cdef int numD = 0
    cdef int isDef = 1
    cdef int numSim = 5000
    cdef np.ndarray[DTYPE_t, ndim=1] R = np.zeros(numSim, dtype=DTYPE) # Rate of incompletion for each simulation

    for i in range(numSim):
        learner = np.random.choice(Nodes)
        is1 = 0
        is2 = 0
        is3 = 0

        # Updates neighbor specialization booleans
        for neighbor in Neighbors[learner]:
            if C[neighbor] == 1:
                is1 = 1
            elif C[neighbor] == 2:
                is2 = 1
            elif C[neighbor] == 3:
                is3 = 1

        # If division of labor is solved in the node's neighborhood
        if is1 == 1 and is2 == 1 and is3 == 1:
            # If threshold is not passed, randomly assign new specialization to node
            if A[learner] < h:
                # if C[learner] == 0:
                C[learner] = np.random.choice([1, 2, 3])
                A[learner] += 1
            else:
                C[learner] = 0
                A[learner] = 0
        
        elif is1 == 1 and is2 == 1 and is3 == 0:
            C[learner] = 3
            A[learner] = 0

        elif is1 == 0 and is2 == 1 and is3 == 1:
            C[learner] = 1
            A[learner] = 0

        elif is1 == 1 and is2 == 0 and is3 == 1:
            C[learner] = 2
            A[learner] = 0

        else:
            if A[learner] < h:
                if is1 == 1:
                    C[learner] = np.random.choice([2, 3])
                elif is2 == 1:
                    C[learner] = np.random.choice([1, 3])
                elif is3 == 1:
                    C[learner] = np.random.choice([1, 2])
                else:
                    if C[learner] == 0:
                        C[learner] = np.random.choice([1, 2, 3])
                A[learner] += 1
            else:
                C[learner] = 0
                A[learner] = 0


        numD = 0 # Number of nodes that have not satisfied DoL
        for k in range(nsize):
            is1 = 0
            is2 = 0
            is3 = 0
            if C[k] == 1:
                is1 = 1
            elif C[k] == 2:
                is2 = 1
            elif C[k] == 3:
                is3 = 1
            for neighbor in Neighbors[k]:
                if C[neighbor] == 1:
                    is1 = 1
                elif C[neighbor] == 2:
                    is2 = 1
                elif C[neighbor] == 3:
                    is3 = 1
            if is1 == 0 or is2 == 0 or is3 == 0:
                numD += 1

        R[i] = numD # Number of incomplete nodes
        if numD == 0:
            break;

    return R

def runWithDL3(G, CD, h):
    # Initializes A (how many times the node has solved DoL, contingent on threshold) as zero arrays
    cdef np.ndarray[DTYPE_t, ndim=1] C = np.zeros(len(G.nodes()), dtype=DTYPE)
    cdef np.ndarray[DTYPE_t, ndim=1] A = np.zeros(len(G.nodes()), dtype=DTYPE)
    cdef dict Neighbors = {}
    cdef int h2 = h # Threshold

    # Initializes C (specialization of each node), same as D in run files
    for n in G.nodes():
        C[n] = CD[n]
        Neighbors[n] = list(G.neighbors(n))

    cdef list Nodes = list(G.nodes())

    return _runWithDL3(Nodes, Neighbors, C, A, h2) # Returns # of incompleted nodes



#########
# Division of labor game with 2 items
#########

cdef np.ndarray[DTYPE_t, ndim=1] _runWithDL2(list Nodes, dict Neighbors, np.ndarray[DTYPE_t, ndim=1] C, np.ndarray[DTYPE_t, ndim=1] A, int h):
    cdef int nsize = len(Nodes)
    cdef int n, neighbor, learner
    cdef int is1, is2
    cdef int numD = 0
    cdef int isDef = 1
    cdef int numSim = 5000
    cdef np.ndarray[DTYPE_t, ndim=1] R = np.zeros(numSim, dtype=DTYPE)
    cdef int dummy = -1

    for i in range(numSim):
        learner = np.random.choice(Nodes)
        is1 = 0
        is2 = 0

        for neighbor in Neighbors[learner]:
            if C[neighbor] == 1:
                is1 = 1
            elif C[neighbor] == 2:
                is2 = 1

        if is1 == 1 and is2 == 1:
            if A[learner] < h:
                C[learner] = np.random.choice([1, 2])
                A[learner] += 1
            else:
                C[learner] = 0
                A[learner] = 0

        elif is1 == 0 and is2 == 1:
            C[learner] = 1
            A[learner] = 0

        elif is1 == 1 and is2 == 0:
            C[learner] = 2
            A[learner] = 0

        else:
            if A[learner] < h:
                if C[learner] == 0:
                    C[learner] = np.random.choice([1, 2])
            else:
                C[learner] = 0
                A[learner] = 0

        numD = 0
        for k in range(nsize):
            is1 = 0
            is2 = 0
            if C[k] == 1:
                is1 = 1
            elif C[k] == 2:
                is2 = 1
            for neighbor in Neighbors[k]:
                if C[neighbor] == 1:
                    is1 = 1
                elif C[neighbor] == 2:
                    is2 = 1
            if is1 == 0 or is2 == 0:
                numD += 1

        R[i] = numD
        if numD == 0:
            break;

    return R

def runWithDL2(G, CD, h):
    cdef np.ndarray[DTYPE_t, ndim=1] C = np.zeros(len(G.nodes()), dtype=DTYPE)
    cdef np.ndarray[DTYPE_t, ndim=1] A = np.zeros(len(G.nodes()), dtype=DTYPE)
    cdef dict Neighbors = {}
    cdef int h2 = h
    for n in G.nodes():
        C[n] = CD[n]
        Neighbors[n] = list(G.neighbors(n))

    cdef list Nodes = list(G.nodes())

    return _runWithDL2(Nodes, Neighbors, C, A, h2)



#########
# Division of labor game with 4 items
#########

cdef np.ndarray[DTYPE_t, ndim=1] _runWithDL4(list Nodes, dict Neighbors, np.ndarray[DTYPE_t, ndim=1] C, np.ndarray[DTYPE_t, ndim=1] A, int h): # with latency
    cdef int nsize = len(Nodes)
    cdef int n, neighbor, learner, k, nei
    cdef int is1, is2, is3, is4
    cdef int numD = 0
    cdef int isDef = 1
    cdef int numSim = 5000
    cdef np.ndarray[DTYPE_t, ndim=1] R = np.zeros(numSim, dtype=DTYPE)

    for i in range(numSim):
        learner = np.random.choice(Nodes)
        is1 = 0
        is2 = 0
        is3 = 0
        is4 = 0

        for neighbor in Neighbors[learner]:
            if C[neighbor] == 1:
                is1 = 1
            elif C[neighbor] == 2:
                is2 = 1
            elif C[neighbor] == 3:
                is3 = 1
            elif C[neighbor] == 4:
                is4 = 1

        if is1 == 1 and is2 == 1 and is3 == 1 and is4 == 1:
            if A[learner] < h:
                if C[learner] == 0:
                    C[learner] = np.random.choice([1, 2, 3, 4])
                A[learner] += 1
            else:
                C[learner] = 0
                A[learner] = 0

        elif is1 == 1 and is2 == 1 and is3 == 0 and is4 == 1:
            C[learner] = 3
            A[learner] = 0

        elif is1 == 0 and is2 == 1 and is3 == 1 and is4 == 1:
            C[learner] = 1
            A[learner] = 0

        elif is1 == 1 and is2 == 0 and is3 == 1 and is4 == 1:
            C[learner] = 2
            A[learner] = 0

        elif is1 == 1 and is2 == 1 and is3 == 1 and is4 == 0:
            C[learner] = 4
            A[learner] = 0


        else:
            if A[learner] < h:
                if is1 == 1 and is2 == 1:
                    C[learner] = np.random.choice([3, 4])
                elif is1 == 1 and is3 == 1:
                    C[learner] = np.random.choice([2, 4])
                elif is1 == 1 and is4 == 1:
                    C[learner] = np.random.choice([2, 3])
                elif is2 == 1 and is3 == 1:
                    C[learner] = np.random.choice([1, 4])
                elif is2 == 1 and is4 == 1:
                    C[learner] = np.random.choice([1, 3])
                elif is3 == 1 and is4 == 1:
                    C[learner] = np.random.choice([1, 2])
                elif is1 == 1:
                    C[learner] = np.random.choice([2, 3, 4])
                elif is2 == 1:
                    C[learner] = np.random.choice([1, 3, 4])
                elif is3 == 1:
                    C[learner] = np.random.choice([1, 2, 4])
                elif is4 == 1:
                    C[learner] = np.random.choice([1, 2, 3])
                else:
                    if C[learner] == 0:
                        C[learner] = np.random.choice([1, 2, 3, 4])
                A[learner] += 1
            else:
                C[learner] = 0
                A[learner] = 0

        numD = 0
        for k in range(nsize):
            is1 = 0
            is2 = 0
            is3 = 0
            is4 = 0
            if C[k] == 1:
                is1 = 1
            elif C[k] == 2:
                is2 = 1
            elif C[k] == 3:
                is3 = 1
            elif C[k] == 4:
                is4 = 1
            for neighbor in Neighbors[k]:
                if C[neighbor] == 1:
                    is1 = 1
                elif C[neighbor] == 2:
                    is2 = 1
                elif C[neighbor] == 3:
                    is3 = 1
                elif C[neighbor] == 4:
                    is4 = 1
            if is1 == 0 or is2 == 0 or is3 == 0 or is4 == 0:
                numD += 1

        R[i] = numD
        if numD == 0:
            break;

    return R

def runWithDL4(G, CD, h):
    cdef np.ndarray[DTYPE_t, ndim=1] C = np.zeros(len(G.nodes()), dtype=DTYPE)
    cdef np.ndarray[DTYPE_t, ndim=1] A = np.zeros(len(G.nodes()), dtype=DTYPE)
    cdef dict Neighbors = {}
    cdef int h2 = h

    for n in G.nodes():
        C[n] = CD[n]
        Neighbors[n] = list(G.neighbors(n))

    cdef list Nodes = list(G.nodes())

    return _runWithDL4(Nodes, Neighbors, C, A, h2)



#########
# Division of labor game with 5 items (only without storage)
#########

cdef np.ndarray[DTYPE_t, ndim=1] _runWithDL5(list Nodes, dict Neighbors, np.ndarray[DTYPE_t, ndim=1] C): # without latency
    cdef int nsize = len(Nodes)
    cdef int n, neighbor, learner, k, nei
    cdef int is1, is2, is3, is4, is5
    cdef int numD = 0
    cdef int isDef = 1
    cdef int numSim = 5000
    cdef np.ndarray[DTYPE_t, ndim=1] R = np.zeros(numSim, dtype=DTYPE)

    for i in range(numSim):
        learner = np.random.choice(Nodes)
        is1 = 0
        is2 = 0
        is3 = 0
        is4 = 0
        is5 = 0

        for neighbor in Neighbors[learner]:
            if C[neighbor] == 1:
                is1 = 1
            elif C[neighbor] == 2:
                is2 = 1
            elif C[neighbor] == 3:
                is3 = 1
            elif C[neighbor] == 4:
                is4 = 1
            elif C[neighbor] == 5:
                is4 = 1

        if is1 == 1 and is2 == 1 and is3 == 1 and is4 == 1 and is5 == 1:
            C[learner] = 0

        elif is1 == 1 and is2 == 1 and is3 == 0 and is4 == 1 and is5 == 1:
            C[learner] = 3

        elif is1 == 0 and is2 == 1 and is3 == 1 and is4 == 1 and is5 == 1:
            C[learner] = 1

        elif is1 == 1 and is2 == 0 and is3 == 1 and is4 == 1 and is5 == 1:
            C[learner] = 2

        elif is1 == 1 and is2 == 1 and is3 == 1 and is4 == 0 and is5 == 1:
            C[learner] = 4

        elif is1 == 1 and is2 == 1 and is3 == 1 and is4 == 1 and is5 == 0:
            C[learner] = 5

        else:
            C[learner] = 0

        numD = 0
        for k in range(nsize):
            is1 = 0
            is2 = 0
            is3 = 0
            is4 = 0
            is5 = 0
            if C[k] == 1:
                is1 = 1
            elif C[k] == 2:
                is2 = 1
            elif C[k] == 3:
                is3 = 1
            elif C[k] == 4:
                is4 = 1
            elif C[k] == 5:
                is5 = 1
            for neighbor in Neighbors[k]:
                if C[neighbor] == 1:
                    is1 = 1
                elif C[neighbor] == 2:
                    is2 = 1
                elif C[neighbor] == 3:
                    is3 = 1
                elif C[neighbor] == 4:
                    is4 = 1
                elif C[neighbor] == 5:
                    is5 = 1
            if is1 == 0 or is2 == 0 or is3 == 0 or is4 == 0 or is5 == 0:
                numD += 1

        R[i] = numD
        if numD == 0:
            break;

    return R

def runWithDL5(G, CD):
    cdef np.ndarray[DTYPE_t, ndim=1] C = np.zeros(len(G.nodes()), dtype=DTYPE)
    cdef dict Neighbors = {}
    for n in G.nodes():
        C[n] = CD[n]
        Neighbors[n] = list(G.neighbors(n))

    cdef list Nodes = list(G.nodes())

    return _runWithDL5(Nodes, Neighbors, C)
