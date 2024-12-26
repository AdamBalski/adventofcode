import collections

data = [list(line) for line in open("/dev/stdin", "r").read().splitlines()]

def bfs(start_i, start_j, visited):
    s = collections.deque([(start_i, start_j)])
    area = 0
    perimeter_lookups = collections.defaultdict(set)
    while s:
        i, j = s.pop()
        if (i, j) in visited:
            continue
        area += 1
        visited.add((i, j))
        for delta_i, delta_j in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_i, new_j = i + delta_i, j + delta_j
            if (new_i < 0 or new_j < 0 or new_i >= len(data) or new_j >= len(data[0])) \
                    or data[start_i][start_j] != data[new_i][new_j]:
                perimeter_lookups[(delta_i, delta_j, new_i if delta_i != 0 else new_j)].add(new_i if delta_i == 0 else new_j)
                continue
            s.append((new_i, new_j))

    perimeter = 0
    for _, sides in perimeter_lookups.items():
        sides_sorted = sorted(sides)
        perimeter += 1
        for i in range(1, len(sides_sorted)):
            if sides_sorted[i] != sides_sorted[i - 1] + 1:
                perimeter += 1
    return area * perimeter
             

result = 0
visited = set()
for i in range(len(data)):
    for j in range(len(data[0])):
        if (i, j) not in visited:
            result += bfs(i, j, visited)
print(result)
