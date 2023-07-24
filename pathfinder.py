from collections import deque
import heapq
import sys
import pdb

# configurate with launch.json file
map_file = sys.argv[1]
algorithm = None
heuristic = None

if len(sys.argv) >= 3:
    algorithm = sys.argv[2]

if len(sys.argv) == 4:
    heuristic = sys.argv[3]


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
    



# print result map
def print_result(path):
    for i in range(rows):
        for j in range(cols):
            if (i, j) == (start_x, start_y):
                print("*", end=" ")
            elif (i, j) in path:
                print("*", end=" ")
            elif grid_map[i][j] == float('inf'):
                print("X", end=" ")
            else:
                print(grid_map[i][j], end=" ")
        print() 


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
    

# bfs algorithem
# check (x, y) is inside the boundry
def is_valid(x, y):
    if x >=0 and x < rows and y >=0 and y < cols and grid_map[x][y] != float('inf'):
        return True
    return False

def bfs():
    #action folloews up, down, left and right order
    action = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    start_node = Node(start_state)

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

        for dx, dy in action:
            new_x, new_y = curr.state[0] + dx, curr.state[1] + dy
            if is_valid(new_x, new_y) and (new_x, new_y) not in explored:
                new_node = Node((new_x, new_y), curr, curr.path_cost + 1)
                que.append(new_node)

    return None




# ucs algorithem
def ucs():
    # action folloews up, down, left and right order
    action = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    start_node = Node(start_state)

    pri_que = []
    explored = set()
    heapq.heappush(pri_que, (start_node.path_cost, -start_node.state[0], -start_node.state[1], start_node))
    
    while pri_que:
        curr = heapq.heappop(pri_que)[3]
        if curr.state == end_state:
            path = []
            while curr.parent is not None:
                path.append(curr.state)
                curr = curr.parent
            return path[::-1]
        explored.add(curr.state)

        for dx, dy in action:
            new_x, new_y = curr.state[0] + dx, curr.state[1] + dy
            if not is_valid(new_x, new_y):
                continue
            if (new_x, new_y) in explored:
                continue
            new_cost = curr.path_cost + grid_map[new_x][new_y]
            new_node = Node((new_x, new_y), curr, new_cost)


            if new_node.state not in [n[3].state for n in pri_que]:
                heapq.heappush(pri_que, (new_cost, -new_node.state[0], -new_node.state[1], new_node))
            elif new_node.state in [n[3].state for n in pri_que]:
                for i, (path_cost, prio1, prio2, old_node) in enumerate(pri_que):
                    if old_node.state == new_node.state:
                        if new_node.path_cost < old_node.path_cost:
                            pri_que[i] = (new_node.path_cost, -new_node.state[0], -new_node.state[1], new_node)
                        break

    return None



# define 2 heuristics methods
from math import sqrt
def euclidean(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return sqrt((x1 - x2)**2 + (y1 - y2)**2)

def manhattan(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


  
# astar algorithem
def astar_manhattan():
    # action folloews up, down, left and right order
    action = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    start_node = Node(start_state)

    pri_que = []
    explored = set()
    heapq.heappush(pri_que, (start_node.path_cost + manhattan(start_state, end_state),  start_node))


    while pri_que:
        curr = heapq.heappop(pri_que)[1]
        if curr.state == end_state:
            path = []
            while curr.parent is not None:
                path.append(curr.state)
                curr = curr.parent
            return path[::-1]
        explored.add(curr.state)

        for dx, dy in action:
            new_x, new_y = curr.state[0] + dx, curr.state[1] + dy
            if not is_valid(new_x, new_y):
                continue
            
            if grid_map[new_x][new_y] > grid_map[curr.state[0]][curr.state[1]]:
                next_cost = grid_map[new_x][new_y] - grid_map[curr.state[0]][curr.state[1]] + 1
            else:
                next_cost = 1

            change = (new_x - curr.state[0], new_y - curr.state[1])
            if change == (1, 0):
                next_cost -= 0.01

            new_cost = curr.path_cost + next_cost
            new_node = Node((new_x, new_y), curr, new_cost)
            new_priority = new_cost + manhattan(new_node.state, end_state)


            if new_node.state not in explored or new_node.state not in [n[1].state for n in pri_que]:
                heapq.heappush(pri_que,(new_priority, new_node))
    
            elif new_node.state in [n[1].state for n in pri_que]:
                for item in pri_que: 
                    if item[1].state == new_node.state and new_priority < item[0]:
                        item = (new_priority, new_node)
                        break
    return None



def astar_euclidean():
    # action folloews up, down, left and right order
    action = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    start_node = Node(start_state)

    pri_que = []
    explored = set()
    heapq.heappush(pri_que, (start_node.path_cost + euclidean(start_state, end_state), -start_node.state[0], -start_node.state[1], start_node))#-start_node.state[0], -start_node.state[1],


    while pri_que:
        curr = heapq.heappop(pri_que)[3]
        if curr.state == end_state:
            path = []
            while curr.parent is not None:
                path.append(curr.state)
                curr = curr.parent
            return path[::-1]
        explored.add(curr.state)

        for dx, dy in action:
            new_x, new_y = curr.state[0] + dx, curr.state[1] + dy
            if not is_valid(new_x, new_y):
                continue
            if (new_x, new_y) in explored:
                continue
            
            if grid_map[new_x][new_y] > grid_map[curr.state[0]][curr.state[1]]:
                next_cost = grid_map[new_x][new_y] - grid_map[curr.state[0]][curr.state[1]] + 1
            else:
                next_cost = 1

            new_cost = curr.path_cost + next_cost
            new_node = Node((new_x, new_y), curr, new_cost)
            new_priority = new_cost + euclidean(new_node.state, end_state)
            

            if new_node.state in [n[3].state for n in pri_que]:
                for item in pri_que: 
                    if item[3].state == new_node.state and new_priority < item[0]:
                        item = (new_priority, -new_node.state[0], -new_node.state[1], new_node)
                        break
            else:
                heapq.heappush(pri_que,(new_priority, -new_node.state[0], -new_node.state[1], new_node))

    return None



# use launch.json to call the code
if algorithm == "bfs":
    path_list_b = bfs()
    if path_list_b == None:
        print("null")
        sys.exit()
    else:
        print_result(path_list_b)
        sys.exit() 


if algorithm == "ucs":
    path_list_u = ucs()
    if path_list_u == None:
        print("null")
        sys.exit()
    else:
        print_result(path_list_u)
        sys.exit() 


if algorithm == "astar" and heuristic == "manhattan":
    path_list_m = astar_manhattan()
    if path_list_m == None:
        print("null")
        sys.exit()
    else:
        print_result(path_list_m)
        sys.exit()


if algorithm == "astar" and heuristic == "euclidean":
    path_list_e = astar_euclidean()
    if path_list_e == None:
        print("null")
        sys.exit()
    else:
        print_result(path_list_e)
        sys.exit()
