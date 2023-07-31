# Path-finding
BFS / UCS /  A* Search / Pathfinding by direct optimisation (simulated annealing)

### input map

example input map is provided, first line is the size of the map, second line is the start location and the third line is the goal location, the rest is the map, `X` means obstacles.

### Problem Formulation

States: Any obstacle-free position (i, j) on the map.
Initial States: A position (i0, j0) given by the user.
Actions: Since we consider 4-connectedness, only four actions are available: Up, down, left and right (your program must expand each node in this order). Available actions for positions adjacent to the map boundary or obstacles are reduced accordingly.
Transition Model: Moving left moves the current position to the left, etc.
Goal Test: Check if the current state is the end position (i*, j*) given by the user.
Path Cost: Given a map M and a Path P{(i0, j0), (i1, j1), ... (iN, jN)}, the cost of the path is calculated as:

$g\left(P\right)=\sum_{k=1}^Nc\left(i_{k-1},j_{k-1},i_k,j_k,M\right)$,

where

$c\left(a,b,c,d,M\right)=\begin{cases}1+M\left(c,d\right)-M\left(a,b\right) & if M(c,d) - M(a, b) > 0\\1 & otherwise \end{cases}$

and M(a, b) is the elevation at the position (a, b). In words, the cost of a path is the sum of the costs between adjacent points in the path, and the cost between adjacent points is 1 plus the difference between the elevation of the two points if we climb "uphill" or simply 1 if we stay "level" or slide "downhill".


code can be called as following:

__>>> python pathfinder.py [map] [algorithm] [heuristic]__

- [algorithm] specifies the search algorithm to use, with the possible values of __bfs__, __ucs__, and __astar__.
- [heuristic] specifies the heuristic to use for A* search, with the possible values of __euclidean__ and __manhattan__. This input is ignored for BFS and UCS.



__>>> python sapathfinder.py [map] [init] [tini] [tfin] [alpha] [d]__

The inputs/options to the program are as follows:

- [map] specifies the path to the map as formatted in `pathfinder.py`
- [init] specifies the path to an initial path, encoded according to the output of the program (as `pathfinder.py`)
- [tini] and [tfin] specify the intial and final temperature respectively.
- [alpha] specifies the cooling rate
- [d] specifies the segment length for random local path adjustments.

*Algorithm Reference Sources: Artificial Intelligence A Modern Approach (Third Edition) --Stuart J. Russell and Peter Norvig*
