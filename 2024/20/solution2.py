import heapq

dirs_by_cnt = {}
dirs_by_cnt[0] = [(0, 0)]
dirs_by_cnt[1] = [(-1, 0), (1, 0), (0, 1), (0, -1)]
seen_dirs = set(dirs_by_cnt[1])
seen_dirs.add((0, 0))
for n in range(2, 21):
    new_set = set()
    for i, j in dirs_by_cnt[1]:
        for di, dj in dirs_by_cnt[n - 1]:
            ni, nj = i + di, j + dj
            if (ni, nj) in seen_dirs:
                continue
            seen_dirs.add((ni, nj))
            new_set.add((ni, nj))
    dirs_by_cnt[n] = new_set


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

def manhattan(i, j, ni, ny):
    return abs(i - ni) + abs(j - ny)

cnt = 0
for i, j in distances:
    for dx, dy in seen_dirs:
        ni, nj = i + dx, j + dy
        if (ni, nj) not in distances:
            continue
        if manhattan(i, j, ni, nj) + distances[(ni, nj)] <= distances[(i, j)] - 100:
            cnt += 1
print(cnt)
