import sys
import collections
sys.path.append('/'.join(__file__.split("/")[:-2]))
import utils

side_len = 71

all_corrupted = list(map(tuple, utils.input_lines("{int},{int}")))

def can_traverse(cnt):
    visited = set()
    corrupted = set(all_corrupted[:cnt])
    q = collections.deque([(0, 0, 0)])
    while q:
        curr_cost, i, j = q.popleft()
        if i < 0 or  j < 0 or i >= side_len or j >= side_len or (i, j) in corrupted:
            continue
        if (i, j) in visited:
            continue
        visited.add((i, j))

        if (i, j) == (side_len - 1, side_len - 1):
            return True
        for delta_i, delta_j in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_i, new_j = i + delta_i, j + delta_j
            q.append((curr_cost + 1, new_i, new_j))
    return False

p = 0
q = len(all_corrupted) - 1

if can_traverse(len(all_corrupted)):
    print("?")
ans = q
while p <= q:
    mid = p + (q - p) // 2
    if can_traverse(mid):
        p = mid + 1
    else:
        q = mid - 1
        ans = mid
print(all_corrupted[ans - 1])
