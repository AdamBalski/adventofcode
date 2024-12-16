import sys
import heapq

at_i, at_j = -1, -1
data = []
for i, line in enumerate(sys.stdin):
    if line == "\n":
        break
    data.append(line)
    if 'S' in data[-1]:
        at_i = i
        at_j = data[-1].find('S')

rotate = {
        (1, 0): [(0, -1), (0, 1)],
        (-1, 0): [(0, 1), (0, -1)],
        (0, 1): [(1, 0), (-1, 0)],
        (0, -1): [(1, 0), (-1, 0)] 
}

# pq is a heap of (cost, i, j, move_i, move_j), where move_i, move_j indicates direction
pq = [(0, at_i, at_j, 0, 1)]
visited = set()

while pq:
    cost, curr_i, curr_j, move_i, move_j = heapq.heappop(pq)
    if curr_i * curr_j < 0 or curr_i >= len(data) or curr_j >= len(data[0]) \
            or data[curr_i][curr_j] == '#' or (curr_i, curr_j, move_i, move_j) in visited:
        continue
    visited.add((curr_i, curr_j, move_i, move_j))

    if data[curr_i][curr_j] == 'E':
        print(cost)
        break

    for new_move_i, new_move_j in rotate[(move_i, move_j)]:
        heapq.heappush(pq, (cost + 1000, curr_i, curr_j, new_move_i, new_move_j))
    heapq.heappush(pq, (cost + 1, curr_i + move_i, curr_j + move_j, move_i, move_j))

