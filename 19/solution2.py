import sys
import collections

avds = next(sys.stdin).rstrip().split(", ")
next(sys.stdin)
designs = [line.rstrip() for line in sys.stdin]

def count_ways(design):
    ways = collections.defaultdict(int)
    ways[0] = 1

    for i in range(1, len(design) + 1):
        for avd in avds:
            if design[i - len(avd):i] != avd:
                continue
            ways[i] += ways[i - len(avd)]
    return ways[len(design)]


result = 0
for i, design in enumerate(designs):
    result += count_ways(design)
print(result)
