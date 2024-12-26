import sys
import collections
import heapq

at_i, at_j = -1, -1
data = []
for i, line in enumerate(sys.stdin):
    if line == "\n":
        break
    data.append(line)
    if 'S' in data[-1]:
        at_i = i
        at_j = data[-1].index('S')


rotate = {
        (1, 0): [(0, -1), (0, 1)],
        (-1, 0): [(0, 1), (0, -1)],
        (0, 1): [(1, 0), (-1, 0)],
        (0, -1): [(1, 0), (-1, 0)] 
}

# move_i is delta between i after and i before a move FORWARD (direction), same for move_j

# pq - heap of (cost, i, j, move_i, move_j)
pq = [(0, at_i, at_j, 0, 1)]
# set of visited (i, j, move_i, move_j) states
visited = set()
# links a (i, j, move_i, move_j, cost) state to a set of states that have incoming states 
#   (for best paths it is guaranteed to only lead to best path nodes)
backlinks = collections.defaultdict(set)
# i, j, move_i, move_j, cost at the E state
last_state = -1, -1, -1, -1

# bfs through the best paths while creating the backlinks dict
while pq:
    cost, curr_i, curr_j, move_i, move_j = heapq.heappop(pq)
    if curr_i * curr_j < 0 or curr_i >= len(data) or curr_j >= len(data[0]) \
            or data[curr_i][curr_j] == '#' or (curr_i, curr_j, move_i, move_j) in visited:
        continue
    visited.add((curr_i, curr_j, move_i, move_j))

    if data[curr_i][curr_j] == 'E':
        last_state = curr_i, curr_j, move_i, move_j, cost
        break

    for new_move_i, new_move_j in rotate[(move_i, move_j)]:
        heapq.heappush(pq, (cost + 1000, curr_i, curr_j, new_move_i, new_move_j))
        backlinks[curr_i, curr_j, new_move_i, new_move_j, cost + 1000].add((curr_i, curr_j, move_i, move_j, cost))
    heapq.heappush(pq, (cost + 1, curr_i + move_i, curr_j + move_j, move_i, move_j))
    backlinks[curr_i + move_i, curr_j + move_j, move_i, move_j, cost + 1].add((curr_i, curr_j, move_i, move_j, cost))

# go through backlinks from the E state to create a set of states in best paths
visited_dfs = set()
def dfs(i, j, move_i, move_j, cost):
    if (i, j, move_i, move_j) in visited_dfs:
        return
    visited_dfs.add((i, j, move_i, move_j))
    for new in backlinks[(i, j, move_i, move_j, cost)]:
        dfs(*new)
dfs(*last_state)
    
# count of 'best path' states grouped by (i, j)
print(len({(i, j) for i, j, _, _ in visited_dfs}))

