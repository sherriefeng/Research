import networkx as nx
import random
import numpy as np
import csv

import numOfSolutionsDepthC
import divisionGame


# solution numbers of division of labour game
def count_solutions(num_trials):
    solution_counts = {}

    for _ in range(num_trials):
        result = _runWithDL3(Nodes, Neighbors, C, A, h)

        # Check if division of labor was achieved
        if result[-1] == 0:  # Division of labor was achieved
            solution = tuple(C)  # Snapshot of the current solution

            if solution in solution_counts:
                solution_counts[solution] += 1
            else:
                solution_counts[solution] = 1

    return solution_counts

print(count_solutions)