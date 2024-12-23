import sys
sys.path.append('/'.join(__file__.split("/")[:-2]))
import utils

class UnionFind:
    def __init__(self):
        self.roots = {}

    def __len__(self):
        return len(self.roots)

    def __contains__(self, x):
        return x in self.roots

    def find(self, p):
        if p not in self.roots:
            self.roots[p] = p
            return p
        while self.roots[p] != p:
            p, self.roots[p] = self.roots[p], self.roots[self.roots[p]]
        return p

    def union(self, p, q):
        p = self.find(p)
        q = self.find(q)
        self.roots[p] = q

    def connected(self, p, q):
        return self.find(p) == self.find(q)

    def subset(self, p):
        # I guess each parent could have linked lists with head and tail pointers instead
        res = []
        for num in self.roots:
            if self.connected(p, num):
                res.append(num)
        return res

    def subsets(self):
        seen = set()
        for node in self.roots:
            if node in seen:
                continue
            curr = self.subset(node)
            for c in curr:
                seen.add(c)
            yield curr

uf = UnionFind()
comps = []
conns = set()
for c1, c2 in list(utils.input_lines("{}-{}")):
    conns.add((c1, c2))
    conns.add((c2, c1))
    comps.append(c1)
    comps.append(c2)
    uf.union(c1, c2)
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
