import sys
import collections

values = {}
def compute(a_name, b_name, gate):
    gates = {}
    gates = {
            "AND": lambda a, b: a & b,
            "OR": lambda a, b: a | b,
            "XOR": lambda a, b: a ^ b,
    }
    return gates[gate](values[a_name], values[b_name])

for line in sys.stdin:
    if line == '\n':
        break
    name, value = line.split(": ")
    values[name] = int(value)

outbound = collections.defaultdict(list)
nodes_to_recipes = {}
indegree = {}
for line in sys.stdin:
    a, gate, b, _, c = line.split()
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

print(get_num('z'))
