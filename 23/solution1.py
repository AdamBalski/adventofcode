import sys
sys.path.append('/'.join(__file__.split("/")[:-2]))
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
for i, c in enumerate(comps):
    for j in range(i + 1, len(comps)):
        if (comps[i], comps[j]) not in conns:
            continue
        for k in range(j + 1, len(comps)):
            if (comps[j], comps[k]) not in conns:
                continue
            if (comps[i], comps[k]) not in conns:
                continue
            if 't' in (comps[i][0], comps[j][0], comps[k][0]):
                cnter += 1


print(cnter)
