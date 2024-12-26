import collections
import random
import math

file = open("./input", "r")
frozen_values = {}
frozen_schema = []
for line in file:
    if line == '\n':
        break
    name, value = line.split(": ")
    frozen_values[name] = int(value)

print("curr swaps:")
SWAPS = [["gws", "nnt"], ["z19", "cph"], ["z13", "npf"], ["z33", "hgj"]]
print(','.join(swapped_gate for swap in SWAPS for swapped_gate in swap))

swaps_dict = {k: v for dictionary in ({x: y, y: x} for x, y in SWAPS) for k, v in dictionary.items()}
for line in file:
    d = line.split()
    if d[-1] in swaps_dict:
        d[-1] = swaps_dict[d[-1]]
    frozen_schema.append(d)

frozen_inbound = collections.defaultdict(set)
for i in range(len(frozen_schema)):
    frozen_inbound[frozen_schema[i][-1]].add(frozen_schema[i][0])
    frozen_inbound[frozen_schema[i][-1]].add(frozen_schema[i][2])
file.close()


GATES = {
        "AND": lambda a, b: a & b,
        "OR": lambda a, b: a | b,
        "XOR": lambda a, b: a ^ b,
}

# get gates whose depentants are in roots, with max depth as max_depth
def get_to(roots, max_depth):
    res = set()
    q = [(root, 0) for root in roots]
    while q:
        curr, depth = q.pop()
        if depth > max_depth:
            continue
        if curr[0] not in ('x', 'y'):
            res.add(curr)
        for c in frozen_inbound[curr]:
            q.append((c, depth + 1))
    return list(res)


def do(x, y, swaps, named_swaps):
    values = {}
    def compute(a_name, b_name, gate):
        return GATES[gate](values[a_name], values[b_name])
    def set_num(name, val):
        idx = 0
        name_with_idx = name + "00"
        while name_with_idx in values:
            values[name_with_idx] = val & 1
            val >>= 1

            idx += 1
            idx_str = str(idx)
            idx_str = "0" * (2 - len(idx_str)) + idx_str
            name_with_idx = name + idx_str

    values = dict(frozen_values)
    set_num('x', x)
    set_num('y', y)

    outbound = collections.defaultdict(list)
    nodes_to_recipes = {}
    indegree = {}
    schema = []
    curr_swaps_dict = {k: v for dictionary in ({x: y, y: x} for x, y in named_swaps) for k, v in dictionary.items()}
    for s in frozen_schema:
        schema.append(list(s))
        if s[-1] in curr_swaps_dict:
            schema[-1][-1] = curr_swaps_dict[s[-1]]
    for i, j in swaps:
        schema[i][-1], schema[j][-1] = schema[j][-1], schema[i][-1]


    for a, gate, b, _, c in schema:
        nodes_to_recipes[c] = a, b, gate
        outbound[a].append(c)
        outbound[b].append(c)
        if c not in indegree:
            indegree[c] = 0
        if a not in values:
            indegree[c] += 1
        if b not in values:
            indegree[c] += 1

    q = [wire for wire in indegree if indegree[wire] == 0]
    while q:
        c_name = q.pop()
        a_name, b_name, gate = nodes_to_recipes[c_name]
        c = compute(a_name, b_name, gate)
        values[c_name] = c
        for wire in outbound[c_name]:
            indegree[wire] -= 1
            if indegree[wire] == 0:
                q.append(wire)

    def get_num(num_name):
        vals = [(wire, val) for wire, val in values.items() if wire[0] == num_name]
        vals.sort(key = lambda a: a[0])
        result = 0
        for i in range(len(vals) - 1, -1, -1):
            val = vals[i][1]
            result *= 2
            result += val
        return result

    res = get_num('z')
    in_x = get_num('x')
    in_y = get_num('y')
    good = in_x + in_y == res
    if good:
        return res, True
    print("wrong!!!")
    def to_powed_log(num):
        if num == 0:
            return "0"
        logged = math.log2(num)
        if int(logged) == logged:
            logged = int(logged)
        return f"2^{logged}"
    print(f"{to_powed_log(in_x)} + {to_powed_log(in_y)} = {to_powed_log(res)}")
    return res, good

# 2 -> "02", 31 -> "31"
def padded(num):
    if num >=10:
        return str(num)
    return "0" + str(num)

# explore possible swaps in this range
swappable = list(get_to(["z" + padded(num) for num in range(10, 15)], 4))
# overwritten to check current swaps (from SWAPS)
# delete to search for fixing swaps
swappable = []
for i in range(len(swappable)):
    for j in range(i, len(swappable)):
        print(swappable[i], swappable[j])
        ok = True
        for k in range(10, 15):
            ok = ok and do(2 ** k, 0, [], [[swappable[i], swappable[j]]])[-1] and\
                        do(0, 2 ** k, [], [[swappable[i], swappable[j]]])[-1] and\
                        do(2 ** k, 2 ** k, [], [[swappable[i], swappable[j]]])[-1]
            if not ok:
                break
        if ok:
            print(swappable[i], swappable[j])
            print("ok")

if swappable != []:
    exit(0)
print("Curr swaps check:")
print("strutural checks")
for k in range(45):
    do(2 ** k, 0, [], [])[-1]
    do(0, 2 ** k, [], [])[-1]
    do(2 ** k, 2 ** k, [], [])[-1]
print("fuzzy checks")
for _ in range(1000):
    do(random.randint(0, 1 << 45), random.randint(0, 1 << 45), [], [])
