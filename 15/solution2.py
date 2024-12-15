import sys

at_i, at_j = -1, -1
data = []
for i, line in enumerate(sys.stdin):
    if line == "\n":
        break
    resize = {'#': '##', '.': '..', '@' : '@.', 'O': '[]'}
    resized = [d for el in line.rstrip() for d in resize[el] if el != '\n']
    data.append(resized)
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

def push(curr_pos, move_dir):
    if at(curr_pos) == '.':
        return True
    if at(curr_pos) == '#':
        return False
    if move_dir in ((0, 1), (0, -1)):
        if push(add(curr_pos, move_dir), move_dir):
            change_at(add(curr_pos, move_dir), at(curr_pos))
            change_at(curr_pos, '.')
            return True
        return False
    # move up or down

    global data

    # in case rollback is needed
    was = [list(line) for line in data]
    # shift is the position of the other bracket wrt. the bracket at curr_pos
    shift = 1 if at(curr_pos) == '[' else -1
    if push(add(curr_pos, move_dir), move_dir) and push(add(curr_pos, add(move_dir, (0, shift))), move_dir):
        change_at(add(curr_pos, move_dir), at(curr_pos))
        change_at(add(curr_pos, add(move_dir, (0, shift))), at(add(curr_pos, (0, shift))))
        change_at(curr_pos, '.')
        change_at(add(curr_pos, (0, shift)), '.')
        return True
    # Rollback in case the second push wasn't successful, but the first was
    data = was
    return False


for move in moves:
    move_dir = {'^': (-1, 0), '>': (0, 1), '<': (0, -1), 'v': (1, 0)}[move]
    if push(add(curr_pos, move_dir), move_dir):
          new = add(curr_pos, move_dir)
          change_at(new, '@')
          change_at(curr_pos, '.')
          curr_pos = new

result = 0
for i in range(len(data)):
    for j in range(len(data[0])):
        if at((i, j)) == '[':
            result += 100 * i + j

print(result)

