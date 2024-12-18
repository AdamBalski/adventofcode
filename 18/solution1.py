import sys
import collections
import itertools
sys.path.append('/'.join(__file__.split("/")[:-2]))
import utils

side_len = 71
bytes_count = 1024

corrupted = set(itertools.islice(map(tuple, utils.input_lines("{int},{int}")), bytes_count))
visited = set()
q = collections.deque([(0, 0, 0)])

while q:
    curr_cost, i, j = q.popleft()
    if i < 0 or j < 0 or i >= side_len or j >= side_len or (i, j) in corrupted:
        continue
    if (i, j) in visited:
        continue
    visited.add((i, j))

    if (i, j) == (side_len - 1, side_len - 1):
        print(curr_cost)
        break
    for delta_i, delta_j in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        new_i, new_j = i + delta_i, j + delta_j
        q.append((curr_cost + 1, new_i, new_j))

