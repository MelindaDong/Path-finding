# path-finding
BFS / UCS /  A* Search / Pathfinding by direct optimisation (simulated annealing)


__>>> python pathfinder.py [map] [algorithm] [heuristic]__

- [algorithm] specifies the search algorithm to use, with the possible values of bfs, ucs, and astar.
- [heuristic] specifies the heuristic to use for A* search, with the possible values of euclidean and manhattan. This input is ignored for BFS and UCS.



__>>> python sapathfinder.py [map] [init] [tini] [tfin] [alpha] [d]__

The inputs/options to the program are as follows:

- [map] specifies the path to the map as formatted in `pathfinder.py`
- [init] specifies the path to an initial path, encoded according to the output of the program (as `pathfinder.py`)
- [tini] and [tfin] specify the intial and final temperature respectively.
- [alpha] specifies the cooling rate
- [d] specifies the segment length for random local path adjustments.
