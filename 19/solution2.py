import sys
import collections

avds = set(next(sys.stdin).rstrip().split(", "))
next(sys.stdin)
designs = [line.rstrip() for line in sys.stdin]
max_avd_len = max(map(len, avds))

def count_ways(design):
    ways = collections.defaultdict(int)
    ways[0] = 1

    for i in range(1, len(design) + 1):
        for avd_len in range(1, min(i, max_avd_len) + 1):
            avd_candidate = design[i - avd_len:i]
            if avd_candidate not in avds:
                continue
            ways[i] += ways[i - avd_len]
    return ways[len(design)]


result = 0
for i, design in enumerate(designs):
    result += count_ways(design)
print(result)
