lines = [line.rstrip() for line in open("/dev/stdin", "r").readlines() if line.strip() != ""]

i, j = -1, -1
for i, line in enumerate(lines):
    j = line.find("^")
    if j != -1:
        break


dir_idx = 0
dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]

visited = set()
while i * j >= 0 and i < len(lines) and j < len(lines[i]):
    if lines[i][j] == "#":
        i, j = i - dirs[dir_idx][0], j - dirs[dir_idx][1]
        dir_idx = (dir_idx + 1) % 4
    visited.add((i, j))
    i, j = i + dirs[dir_idx][0], j + dirs[dir_idx][1]

print(len(visited))
