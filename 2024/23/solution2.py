import sys
sys.path.append('/'.join(__file__.split("/")[:-3]))
import utils

comps = []
conns = set()
for c1, c2 in list(utils.input_lines("{}-{}")):
    conns.add((c1, c2))
    conns.add((c2, c1))
    comps.append(c1)
    comps.append(c2)
comps = list(set(comps))

cnter = 0
lans = [[]]
for i, c in enumerate(comps):
    for j in range(len(lans)):
        bad = False
        for other in lans[j]:
            if (c, other) not in conns:
                bad = True
                break
        if bad:
            continue
        lans.append(lans[j] + [c])
best = []
for lan in lans:
    if len(lan) > len(best):
        best = lan
print(','.join(sorted(best)))

