import collections

data = [list(line) for line in open("/dev/stdin", "r").read().splitlines()]

def bfs(start_i, start_j, visited):
    q = collections.deque([(start_i, start_j)])
    area = 0
    perimeter = 0
    while q:
        i, j = q.popleft()
        if (i, j) in visited:
            continue
        area += 1
        visited.add((i, j))
        for delta_i, delta_j in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_i, new_j = i + delta_i, j + delta_j
            if new_i * new_j < 0 or new_i >= len(data) or new_j >= len(data[0]):
                perimeter += 1
                continue
            if data[start_i][start_j] != data[new_i][new_j]:
                perimeter += 1
                continue
            q.append((new_i, new_j))

    return area * perimeter
             

result = 0
visited = set()
for i in range(len(data)):
    for j in range(len(data[0])):
        if (i, j) not in visited:
            result += bfs(i, j, visited)
print(result)
