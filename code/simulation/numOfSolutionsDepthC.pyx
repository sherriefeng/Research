import numpy as np
cimport numpy as np

DTYPE = np.int64
ctypedef np.int64_t DTYPE_t

cdef dict M = {} # G's adjacency list, node:neighbors (by UID)
cdef dict C = {} # Dictionary of rank:possible colors
cdef POSSIBLE_COLORS = [3, 2, 1]

cdef int depthFirstSearch(int start, int goal):
	cdef int numSolutions = 0
	cdef np.ndarray[DTYPE_t, ndim = 1] stack = np.zeros(goal + 1, dtype = DTYPE) # Stack is an array of n zeroes
	cdef int rank = start				# Rank represents the current node's ID, sorted by degree!!!
	cdef int color						# Color of the current node
	cdef list candidates				# Candidate colors for neighboring nodes
	stack[rank] = C[start].pop()		# Stack is an array of rank:current list of possible colors (first node = 1)
	while 1:
		if numSolutions * 3 > 1000000:	# EVERY COMBINATION HAS 3 POSSIBLE CHOICES, SO YOU MULTIPLY BY 3
			return numSolutions			

		if not C[rank + 1]:				# Case: You reach rank = n-1 / If the next node's color does not exist
			if rank == start:			# Edge case: Graph only has one node
				return numSolutions		# Return numSolutions if we're at the first node
			else:						# Backtrack! Ultimately this returns above and adds an additional node to C?
				stack[rank] = 0			# Resets the current node's color
				C[rank + 1] = [3, 2, 1] # Initialize; sets the next node's possible colors
				rank -= 1

		else:
			color = C[rank + 1].pop() # Arbitrarily choose (pop) a color
			# Question: is "x < rank + 1" just an optimization step? Or is it necessary?
			# Answer: This is DFS; if a node that has more neighbors (higher rank) is also a neighbor, append its candidate colors
			candidates = [stack[x] for x in M[rank + 1] if x < rank + 1]

			# Graph coloring: If the popped color is not already present (it's still needed among neighbors)
			if color not in candidates: # not conflict
				if rank + 1 == goal:
					numSolutions += 1
				else:
					stack[rank + 1] = color
					rank += 1

cdef np.ndarray[DTYPE_t, ndim=1] depthSearchStuckSample(int start, int goal):
	cdef int numSolutions = 0
	cdef np.ndarray[DTYPE_t, ndim=1] stack = np.zeros(goal + 1, dtype=DTYPE)
	cdef int rank = start
	cdef int color
	cdef list candidates
	stack[rank] = C[start].pop()
	while 1:
		if not C[rank + 1]:
			if rank == start:
				return stack
			else:
				stack[rank] = 0
				# Differs from DFS on line below
				C[rank + 1] = np.random.shuffle([3, 2, 1]) # initialize
				rank -= 1

		else:
			color = C[rank + 1].pop()
			candidates = [stack[x] for x in M[rank + 1] if x < rank + 1]
			if color not in candidates: # not conlict
				if rank + 1 == goal:
					# Differs from DFS in this branch
					if numSolutions == 0: # random
						stack[rank + 1] = color
						return stack
					else:
						numSolutions += 1
						print numSolutions
				else:
					stack[rank + 1] = color
					rank += 1


cdef int _getNumOfSolutions(G, dict D):
	""" Helper function for getNumOfSolutions, takes in G (original graph) and D (node:degree dictionary)"""

	cdef dict ID = {} 	# Unique ID for each node; ID = 0 means most neighbers / highest degree
	cdef int uid = 0 	# ID counter
	cdef int n, i
	cdef int numOneDegree = 0

	# Sort the nodes by degree in descending order
	for k, v in sorted(D.items(), key=lambda x:x[1], reverse=True):
		ID[k] = uid
		uid += 1

	# Populate M (adjacency list) with node:neighbors by UID
	for k, v in ID.items():
		M[v] = [ID[x] for x in G.neighbors(k)]

	n = len(G.nodes()) # n is number of nodes in G

	# Populate C with node number(aka rank):array of three possible colors
	C[0] = [1] # Sets the first node's color arbitrarily, which gets popped first
	for i in range(1, n):
		C[i] = [3, 2, 1] # Does this mean the chromatic number is always 3?

	# Why is this multiplied by 3? Answer: Given 3 colors, there are always 3 different combinations of a solution
	return depthFirstSearch(0, n-1) * 3

def getNumOfSolutions(G):
	D = {}
	# D is a dictionary mapping the node to the number of edges (Degree)
	for k, v in G.degree():
		D[k] = v
	return _getNumOfSolutions(G, D)


cdef dict _getSampleCombination(G, dict D):
	cdef dict ID ={}
	cdef int uid = 0
	cdef int n, i
	cdef int numOneDegree = 0

	for i in G.nodes():
		D[i] = G.degree[i]

	for k, v in sorted(D.items(), key=lambda x:x[1], reverse=True):
		ID[k] = uid
		uid += 1

	for k, v in ID.items():
		M[v] = [ID[x] for x in G.neighbors(k)]

	n = len(G.nodes())
	C[0] =[1]
	for i in range(1, n):
		C[i] = [3, 2, 1]

	cdef np.ndarray[DTYPE_t, ndim=1] carray = depthSearchStuckSample(0, n-1)
	cdef dict cdict = {}
	for k, v in ID.items():
		cdict[k] = carray[v]
	return cdict

def getSampleCombination(G):
	D = {}
	for k, v in G.degree():
		D[k] = v
	return _getSampleCombination(G, D)


cdef np.ndarray[DTYPE_t, ndim=1] depthSearchStuckSample2(int start, int goal, int num):
	cdef int numSolutions = 0
	cdef np.ndarray[DTYPE_t, ndim=1] stack = np.zeros(goal + 1, dtype=DTYPE)
	cdef int rank = start
	cdef int color
	cdef list candidates
	stack[rank] = C[start].pop()
	while 1:
		if not C[rank + 1]:
			if rank == start:
				return stack
			else:
				stack[rank] = 0
				C[rank + 1] = [3, 2, 1] #initialize
				rank -= 1

		else:
			color = C[rank + 1].pop()
			candidates = [stack[x] for x in M[rank + 1] if x < rank + 1]
			if color not in candidates: # not conlict
				if rank + 1 == goal:
					# This is where the new parameter "num" is used
					if numSolutions == num: # random (This isn't random though, it's set in examine_completion.py)
						stack[rank + 1] = color
						return stack
					else:
						numSolutions += 1
				else:
					stack[rank + 1] = color
					rank += 1

cdef dict _getSampleCombination2(G, dict D, int num):
	cdef dict ID ={}
	cdef int uid = 0
	cdef int n, i
	cdef int numOneDegree = 0

	for i in G.nodes():
		D[i] = G.degree[i]

	for k, v in sorted(D.items(), key=lambda x:x[1], reverse=True):
		ID[k] = uid
		uid += 1

	for k, v in ID.items():
		M[v] = [ID[x] for x in G.neighbors(k)]

	n = len(G.nodes())
	C[0] =[1]
	for i in range(1, n):
		C[i] = [3, 2, 1]

	cdef np.ndarray[DTYPE_t, ndim=1] carray = depthSearchStuckSample2(0, n-1, num)
	cdef dict cdict = {}
	for k, v in ID.items():
		cdict[k] = carray[v]
	return cdict

def getSampleCombination2(G, num):
	D = {}
	for k, v in G.degree():
		D[k] = v
	return _getSampleCombination2(G, D, num)
