lines = [list(line.rstrip()) for line in open("/dev/stdin", "r").readlines() if line.strip() != ""]

start_i, start_j = -1, -1
for start_i, line in enumerate(lines):
    try:
        start_j = line.index("^")
    except:
        pass
    if start_j != -1:
        break
lines[start_i][start_j] = "^"


dir_idx = 0
dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]

i, j = start_i, start_j
visited = set()
while i * j >= 0 and i < len(lines) and j < len(lines[i]):
    if lines[i][j] == "#":
        i, j = i - dirs[dir_idx][0], j - dirs[dir_idx][1]
        dir_idx = (dir_idx + 1) % 4
    visited.add((i, j))
    i, j = i + dirs[dir_idx][0], j + dirs[dir_idx][1]

def contains_loop(i, j):
    dir_idx = 0
    visited = set()

    while i * j >= 0 and i < len(lines) and j < len(lines[i]):
        if lines[i][j] == "#":
            i, j = i - dirs[dir_idx][0], j - dirs[dir_idx][1]
            dir_idx = (dir_idx + 1) % 4
        if (i, j, dir_idx) in visited:
            return True
        visited.add((i, j, dir_idx))
        i, j = i + dirs[dir_idx][0], j + dirs[dir_idx][1]
    return False
    

result = 0
for i, j in visited:
    lines[i][j] = "#"
    if contains_loop(start_i, start_j):
        result += 1
    lines[i][j] = "."
print(result)
