import sys
import re

def calc(text):
    print(text)
    res = 0
    for match in re.finditer(r"mul\(([0-9]+),([0-9]+)\)", text):
        res += int(match.group(1)) * int(match.group(2))
    return res
        
def calc_prog(text):
    res = 0
    for group in text.split("do()"):
        stop_idx = group.find("don't()")
        if stop_idx == -1:
            stop_idx = len(group)
        res += calc(group[:stop_idx])
    return res

res = 0
text = []
for line in sys.stdin:
    text.append(line)
print(calc_prog(r'\n'.join(text)))
