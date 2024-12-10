import collections

lines = [[int(num) for num in line] for line in open("/dev/stdin").read().splitlines()]

scores = collections.defaultdict(int)
q = collections.deque()
for i in range(len(lines)):
    for j in range(len(lines[0])):
        if lines[i][j] == 0:
            scores[(i, j)] += 1
            q.appendleft((i, j))

visited = set()
while q:
    i, j = q.pop()
    if (i, j) in visited:
        continue
    visited.add((i, j))
    for delta_x, delta_y in ((-1, 0), (1, 0), (0, 1), (0, -1)):
        next_i, next_j = i + delta_x, j + delta_y
        if next_i * next_j < 0 or next_i >= len(lines) or next_j >= len(lines[0]):
            continue
        if lines[next_i][next_j] != lines[i][j] + 1:
            continue
        q.appendleft((next_i, next_j))
        scores[(next_i, next_j)] += scores[(i, j)]

result = 0
for i in range(len(lines)):
    for j in range(len(lines[0])):
        if lines[i][j] == 9:
            result += scores[(i, j)]
print(result)
            

            
