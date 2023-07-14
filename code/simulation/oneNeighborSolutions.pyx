import numpy as np
cimport numpy as np

DTYPE = np.int64
ctypedef np.int64_t DTYPE_t

cdef dict M = {}  # G's adjacency list, node:neighbors (by UID)
cdef dict C = {}  # Dictionary of rank:possible colors
cdef POSSIBLE_COLORS = [3, 2, 1]

cdef int depthFirstSearch(int start, int goal):
    cdef int numSolutions = 0
    cdef np.ndarray[DTYPE_t, ndim=1] stack = np.zeros(goal + 1, dtype=DTYPE)  # Stack is an array of n zeroes
    cdef int rank = start  # Rank represents the current node's ID, sorted by degree!!!
    cdef int color  # Color of the current node
    cdef list candidates  # Candidate colors for neighboring nodes
    stack[rank] = C[start].pop()  # Stack is an array of rank:current list of possible colors (first node = 1)
    
    while 1:
        if numSolutions * len(POSSIBLE_COLORS) > 1000000:  # EVERY COMBINATION HAS len(POSSIBLE_COLORS) POSSIBLE CHOICES
            return numSolutions

        #print "C:", C
        #print "stack:", stack
        #print "rank:", rank

        if not C[rank + 1]:  # Case: You reach rank = n-1 / If the next node's color does not exist
            if rank == start:  # Edge case: Graph only has one node
                return numSolutions  # Return numSolutions if we're at the first node
            else:  # Backtrack! Ultimately this returns above and adds an additional node to C?
                stack[rank] = 0  # Resets the current node's color
                C[rank + 1] = POSSIBLE_COLORS.copy()  # Initialize; sets the next node's possible colors
                rank -= 1

        else:
            color = C[rank + 1].pop()  # Arbitrarily choose (pop) a color
            # Question: is "x < rank + 1" just an optimization step? Or is it necessary?
            # Answer: This is DFS; if a node that has more neighbors (higher rank) is also a neighbor, append its neighbor colors
            neighbors = [stack[x] for x in M[rank + 1] if x < rank + 1]
            #print "color:", color, "neighbors:", neighbors

            # One-Neighbor Coloring: If the popped color is not already present among neighbors
            if len(neighbors) == 0 or any(neighbor != color for neighbor in neighbors):
                if rank + 1 == goal:
                    #print "found a solution!"
                    numSolutions += 1
                else:
                    #print "assigned a color"
                    stack[rank + 1] = color
                    rank += 1


cdef int _getNumOfSolutions(G, dict D):
    """ Helper function for getNumOfSolutions, takes in G (original graph) and D (node:degree dictionary)"""

    cdef dict ID = {}  # Unique ID for each node; ID = 0 means most neighbors / highest degree
    cdef int uid = 0  # ID counter
    cdef int n, i
    cdef int numOneDegree = 0

    # Sort the nodes by degree in descending order
    for k, v in sorted(D.items(), key=lambda x: x[1], reverse=True):
        ID[k] = uid
        uid += 1

    # Populate M (adjacency list) with node:neighbors by UID
    for k, v in ID.items():
        M[v] = [ID[x] for x in G.neighbors(k)]

    n = len(G.nodes())  # n is number of nodes in G

    # Populate C with node number (aka rank):array of possible colors
    C[0] = [1]  # Sets the first node's color arbitrarily, which gets popped first
    for i in range(1, n):
        C[i] = POSSIBLE_COLORS.copy()  # Use the list of possible colors for one-neighbor coloring

    # Multiply by len(POSSIBLE_COLORS) to account for all possible combinations
    return depthFirstSearch(0, n - 1) * len(POSSIBLE_COLORS)


def getNumOfSolutions(G):
    D = {}
    # D is a dictionary mapping the node to the number of edges (Degree)
    for k, v in G.degree():
        D[k] = v
    return _getNumOfSolutions(G, D)
