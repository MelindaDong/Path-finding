import sys
#call by python sapathfinder.py [init] [tini] [tfin] [alpha] [d]

map_file = sys.argv[1]
init = sys.argv[2]
tini = float(sys.argv[3])
tfin = float(sys.argv[4])
alpha = float(sys.argv[5])
d = int(sys.argv[6])


import random
import math
from collections import deque

# extract path from previous output
with open(init, 'r') as file:
    lines = file.readlines()

map_row = []
for line in lines:
    map_row.append(line.strip().split())

init_path = []
for i in range(len(map_row)):
    for j in range(len(map_row[i])):
        if map_row[i][j] == '*':
            init_path.append((i,j))


# read the map
with open(map_file, 'r') as file:
    lines = file.readlines()

map_row = []
for line in lines:
    map_row.append(line.strip().split())

for i in range(len(map_row)):
    for j in range(len(map_row[i])):
        if map_row[i][j] == 'X':
            map_row[i][j] = float('inf')
        else:
            map_row[i][j] = int(map_row[i][j])


grid_map = map_row[3:]
rows, cols = map_row[0][0], map_row[0][1]

start_x, start_y = map_row[1][0]-1, map_row[1][1]-1
start_state = (start_x, start_y)
end_x, end_y = map_row[2][0]-1, map_row[2][1]-1
end_state = (end_x, end_y)



# define child node class
class Node:
    def __init__(self, state, parent = None, path_cost = 0):
        self.state = state
        self.parent = parent
        self.path_cost = path_cost

    # compare two Node objects based on their path_cost attribute. 
    # This allows you to compare two Node objects using the < operator
    def __lt__(self, other):
        return self.path_cost < other.path_cost
    
    def __eq__(self, other):
        return self.state == other.state
    


# check (x, y) is inside the boundry and valid
def is_valid(x, y):
    if x >=0 and x < rows and y >=0 and y < cols and grid_map[x][y] != float('inf'):
        return True
    return False

# convert path into graph
def print_result(path):
    for i in range(rows):
        for j in range(cols):
            if (i, j) == (start_x, start_y):
                print("*", end=" ")
            # elif (i, j) == (end_x, end_y):
            #     print("*", end=" ")
            elif (i, j) in path:
                print("*", end=" ")
            elif grid_map[i][j] == float('inf'):
                print("X", end=" ")
            else:
                print(grid_map[i][j], end=" ")
        print() 


## random bfs algorithem
def randomised_BFS(start, end, grid_map):
    #action folloews up, down, left and right order
    action = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    start_node = Node(start)
    end_state = end

    que = deque()
    explored = set()
    que.append(start_node)
    
    while que:
        curr = que.popleft()
        if curr.state == end_state:
            path = []
            while curr.parent is not None:
                path.append(curr.state)
                curr = curr.parent
            return path[::-1]
        explored.add(curr.state)
        
        #choose random direction
        random.shuffle(action)
        for dx, dy in action:
            new_x, new_y = curr.state[0] + dx, curr.state[1] + dy
            if is_valid(new_x, new_y) and (new_x, new_y) not in explored:
                new_node = Node((new_x, new_y), curr, curr.path_cost + 1)
                que.append(new_node)

    return None


# calculate the cost of a list of path
def get_path_cost(path):
    all_cost = 0
    for i in range(len(path)-1):
        x1, y1 = path[i]
        x2, y2 = path[i + 1]
        if grid_map[x2][y2] > grid_map[x1][y1]:
            all_cost = all_cost + (grid_map[x2][y2] - grid_map[x1][y1] + 1)
        else:
            all_cost += 1
    return all_cost


# generate adjusted path
def adjust_path(P_0, d):
    random_start = random.choice(P_0)
    start_index = P_0.index(random_start)
    if start_index + d < len(P_0):
        end_index = start_index + d
    else:
        end_index = len(P_0) - 1
    random_end = P_0[end_index]
    random_path = randomised_BFS(random_start, random_end, grid_map)
    P_h = P_0[:]
    P_h[start_index + 1 :end_index + 1 ] = random_path
    
    return P_h


# the main simulated annealing algorithm
bookkeeping = []
def simulated_annealing(P_0, Tini, Tfin, alpha, d):
    """Peforms simulated annealing to find a solution"""
    initial_temp = Tini
    final_temp = Tfin
    
    current_temp = initial_temp

    # Start by initializing the current state with the initial state
    P = P_0
    while current_temp > final_temp:
        P_h = adjust_path(P, d)
        cost_P_h = get_path_cost(P_h)
        cost_P = get_path_cost(P)
        cost_diff = cost_P - cost_P_h
        if cost_diff > 0:
            P = P_h
        else:
            if random.uniform(0, 1) < math.exp(cost_diff / current_temp):
                P = P_h
        # add book keeping here
        cost_P = get_path_cost(P)
        bookkeeping.append("T = {0:.6f}, cost = {1}".format(current_temp, cost_P))
        current_temp = alpha * current_temp

    return P



P = simulated_annealing(init_path, tini, tfin, alpha, d) # init_path is the path extracted from init 

print_result(P)
for lines in bookkeeping:
    print(lines)
sys.exit()



