import sys
import re

def calc(text):
    res = 0
    for match in re.finditer(r"mul\(([0-9]+),([0-9]+)\)", text):
        res += int(match.group(1)) * int(match.group(2))
    return res
        

res = 0
for line in sys.stdin:
    res += calc(line)

print(res)
