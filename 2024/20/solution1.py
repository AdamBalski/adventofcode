import heapq

grid = list(open("/dev/stdin", "r").read().splitlines())
si, sj = -2, -2
for i in range(len(grid)):
    for j in range(len(grid[0])):
        if grid[i][j] == 'S':
            si, sj = i, j

distances = {}
pq = [(1, si, sj)]
while pq:
    c, i, j = pq.pop()
    distances[(i, j)] = c
    new_c = 10 ** 10
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        ni, nj = i + dx, j + dy
        if ni < 0 or nj < 0 or ni >= len(grid) or nj >= len(grid[0]):
            continue
        if grid[ni][nj] == '#':
            continue
        if (ni, nj) in distances:
            new_c = min(new_c, distances[(ni, nj)] + 1)
            continue
        heapq.heappush(pq, (1 + c, ni, nj))

cnt = 0
for i, j in distances:
    for dx, dy in [(1, 1), (1, -1), (-1, 1), (-1, -1), (2, 0), (-2, 0), (0, 2), (0, -2)]:
        ni, nj = i + dx, j + dy
        if (ni, nj) not in distances:
            continue
        if 2 + distances[(ni, nj)] <= distances[(i, j)] - 100:
            cnt += 1
print(cnt)

