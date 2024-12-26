import sys

# returns compressed schematic and bool that is True iff the schematic describes a lock
def convert_schematic(schematic):
    res = []
    for i in range(len(schematic[0])):
        j = 0
        while schematic[j][i] == schematic[j + 1][i]:
            j += 1
        res.append(j)
    return res, schematic[0][0] == '#'

schematics = []
while True:
    curr_schematic = []
    for line in sys.stdin:
        if line == "\n":
            break
        curr_schematic.append(line.rstrip())
    if len(curr_schematic) <= 1:
        break
    schematics.append(convert_schematic(curr_schematic))

cnt = 0
for s1 in schematics:
    if not s1[1]:
        continue
    for s2 in schematics:
        if s2[1]:
            continue
        if all(p1 <= p2 for p1, p2 in zip(s1[0], s2[0])):
            cnt += 1
print(cnt)
