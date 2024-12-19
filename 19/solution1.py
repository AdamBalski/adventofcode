import sys

avds = next(sys.stdin).rstrip().split(", ")
next(sys.stdin)
designs = [line.rstrip() for line in sys.stdin]

def can_design(design):
    possible = {0}
    for i in range(1, len(design) + 1):
        for avd in avds:
            if design[i - len(avd):i] != avd:
                continue
            if i - len(avd) not in possible:
                continue
            possible.add(i)
    return len(design) in possible

result = 0
for i, design in enumerate(designs):
    if can_design(design):
        result += 1
print(result)
