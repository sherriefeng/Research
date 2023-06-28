# import numpy as np
cimport numpy as np

DTYPE = np.int64
ctypedef np.int64_t DTYPE_t

cdef dict M = {}
cdef dict C = {}

cdef int depthFirstSearch(int start, int goal):
	cdef int numSolutions = 0
	cdef np.ndarray[DTYPE_t, ndim=1] stack = np.zeros(goal + 1, dtype=DTYPE)
	cdef int rank = start
	cdef int color
	cdef list candidates
	stack[rank] = C[start].pop()
	while 1:
		if numSolutions * 3 > 1000000:
			return numSolutions

		if not C[rank + 1]:
			if rank == start:
				return numSolutions
			else:
				stack[rank] = 0
				C[rank + 1] = [3, 2, 1] #initialize
				rank -= 1

		else:
			color = C[rank + 1].pop()
			candidates = [stack[x] for x in M[rank + 1] if x < rank + 1]
			if color not in candidates: #not conlict
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
				C[rank + 1] = np.random.shuffle([3, 2, 1]) #initialize
				rank -= 1

		else:
			color = C[rank + 1].pop()
			candidates = [stack[x] for x in M[rank + 1] if x < rank + 1]
			if color not in candidates: #not conlict
				if rank + 1 == goal:
					if numSolutions == 0: #random
						stack[rank + 1] = color
						return stack
					else:
						numSolutions += 1
						print numSolutions
				else:
					stack[rank + 1] = color
					rank += 1


cdef int _getNumOfSolutions(G, dict D):
	cdef dict ID ={}
	cdef int uid = 0
	cdef int n, i
	cdef int numOneDegree = 0

	for k, v in sorted(D.items(), key=lambda x:x[1], reverse=True):
		ID[k] = uid
		uid += 1

	for k, v in ID.items():
		M[v] = [ID[x] for x in G.neighbors(k)]

	n = len(G.nodes())
	C[0] =[1]
	for i in range(1, n):
		C[i] = [3, 2, 1]
	return depthFirstSearch(0, n-1) * 3

def getNumOfSolutions(G):
	D = {}
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
			if color not in candidates: #not conlict
				if rank + 1 == goal:
					if numSolutions == num: #random
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
