# Cython codes
- numOfSolutionsDepthC.pyx
	Calculate the solution number of graph coloring with 3 colors.
	Run "python setup_i1.py build_ext --inplace" to create the c code and so object.

- numOfSolutionsDepthCItem4.pyx
	Calculate the solution number of graph coloring with 4 colors.
	Run "python setup_i4.py build_ext --inplace" to create the c code and so object.

- divisionGame.pyx
	Run a simulation of the divison-of-labor game with 2, 3, 4, and 5 items
	The outcome variable is the number of agents who do not have a complete set of items with neighbors.
	Run "python setup.py build_ext --inplace" to create the c code and so object.

- divisionGame.pyx
	Calculate the solution number of the one neighbor game with 3 colors
	Run "python setup_on.py build_ext --inplace" to create the c code and so object.

# Python codes
- generate_networks.py
	Generate a network topology of small-world or preferential attachment network and record it as edge list.

- examine_completion.py
	Calculate the average number of nodes who have a complete set of items with neighbors among the fully colored networks.

- run_small_world_s0.py
	Run the simulations of the divison-of-labor game with a ring lattice network.

- run_small_world_s2.py
	Run the simulations of the divison-of-labor game with two-shortcuts ring lattice networks.

- run_small_world_s6.py
	Run the simulations of the divison-of-labor game with six-shortcuts ring lattice networks.

- run_pref_attach_2.py
	Run the simulations of the divison-of-labor game with preferential attachment networks with v=2.

- run_pref_attach_3.py
	Run the simulations of the divison-of-labor game with preferential attachment networks with v=3.

- run_real_network.py
	Run the simulations of the divison-of-labor game with a real-world (taro-exchange) network.