import sys
import collections

rules = collections.defaultdict(lambda: [])
udpates = []
for line in sys.stdin:
    line = line.strip()
    if line == "":
        break
    curr = [int(num) for num in line.split("|")]
    rules[curr[0]].append(curr[1])

result = 0
for line in sys.stdin:
    curr = [int(num) for num in line.split(",")]
    prev = set()
    bad = False
    for num in curr:
        for required_after in rules[num]:
            if required_after in prev:
                bad = True
                break
        prev.add(num)
    if bad:
        continue
    result += curr[len(curr) // 2]
print(result)

    




