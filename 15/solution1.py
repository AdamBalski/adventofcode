import sys

at_i, at_j = -1, -1
data = []
for i, line in enumerate(sys.stdin):
    if line == "\n":
        break
    data.append(list(line.rstrip()))
    if '@' in data[-1]:
        at_i = i
        at_j = data[-1].index('@')

moves = []
for line in sys.stdin:
    moves.extend(line.rstrip())

def add(a, b):
    return a[0] + b[0], a[1] + b[1]
def times(a, b):
    return b * a[0], b * a[1]
def at(pos):
    return data[pos[0]][pos[1]]
def change_at(pos, a):
    data[pos[0]][pos[1]] = a

curr_pos = at_i, at_j
for move in moves:
    move_dir = {'^': (-1, 0), '>': (0, 1), '<': (0, -1), 'v': (1, 0)}[move]
    i = 1
    while at((new := add(curr_pos, times(move_dir, i)))) == 'O':
        i += 1
    if at(new) == '#':
        continue
    change_at(curr_pos, '.')
    change_at(new, 'O')
    change_at(add(curr_pos, move_dir), '@')
    curr_pos = add(curr_pos, move_dir)

result = 0
for i in range(len(data)):
    for j in range(len(data[0])):
        if at((i, j)) == 'O':
            result += 100 * i + j

print(result)

