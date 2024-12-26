import collections
import itertools

inputt = [line.rstrip() for line in open("/dev/stdin", "r").readlines()]

antennas = collections.defaultdict(set)
for i in range(len(inputt)):
    for j in range(len(inputt[0])):
        if inputt[i][j] != ".":
            antennas[inputt[i][j]].add((i, j))

def distance_squared(p1, p2):
    return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2

def contains_antinode(i, j):
    for _, antenna_set in antennas.items():
        distances_squared = collections.defaultdict(list)
        for antenna in antenna_set:
            curr_distance_squared = distance_squared(antenna, (i, j))
            twice_closer_antennas = distances_squared[curr_distance_squared // 4] if curr_distance_squared % 4==0 else []
            for other in itertools.chain(distances_squared[4 * curr_distance_squared], twice_closer_antennas):
                # if in line
                if other[0] == i == antenna[0] or (i - other[0]) * (antenna[1] - j) == (antenna[0] - i) * (j - other[1]):
                    return True
            distances_squared[curr_distance_squared].append(antenna)
    return False

result = 0
for i in range(len(inputt)):
    for j in range(len(inputt[0])):
        if contains_antinode(i, j):
            result += 1
print(result)

