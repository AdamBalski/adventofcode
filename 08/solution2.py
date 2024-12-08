import collections

inputt = [line.rstrip() for line in open("/dev/stdin", "r").readlines()]

antennas = collections.defaultdict(set)
for i in range(len(inputt)):
    for j in range(len(inputt[0])):
        if inputt[i][j] != ".":
            antennas[inputt[i][j]].add((i, j))

def contains_antinode(i, j):
    for _, antenna_set in antennas.items():
        past_antennas = list()
        for antenna in antenna_set:
            for other in past_antennas:
                # if in line
                if other[0] == i == antenna[0] or \
                        (i - other[0]) * (antenna[1] - j) == (antenna[0] - i) * (j - other[1]):
                    return True
            past_antennas.append(antenna)
    return False

result = 0
for i in range(len(inputt)):
    for j in range(len(inputt[0])):
        if contains_antinode(i, j):
            result += 1
print(result)

