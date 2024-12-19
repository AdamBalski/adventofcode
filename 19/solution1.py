import sys

avds = set(next(sys.stdin).rstrip().split(", "))
next(sys.stdin)
designs = [line.rstrip() for line in sys.stdin]
max_avd_len = max(map(len, avds))

def can_design(design):
    possible = {0}
    for i in range(1, len(design) + 1):
        for avd_len in range(1, min(i, max_avd_len) + 1):
            if i - avd_len not in possible:
                continue
            avd_candidate = design[i - avd_len:i]
            if avd_candidate not in avds:
                continue
            possible.add(i)
            break
    return len(design) in possible

result = 0
for i, design in enumerate(designs):
    if can_design(design):
        result += 1
print(result)
