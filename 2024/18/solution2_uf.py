import sys
sys.path.append('/'.join(__file__.split("/")[:-3]))
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

    def add(self, p):
        if p in self.roots:
            return
        self.roots[p] = p


corrupted_bytes = map(tuple, utils.input_lines("{int},{int}"))
uf = UnionFind()
side_len = 71

# use -1 as the top and right sides,
#     -2 as the bottom and left sides
# start connectiong fallen bytes octo-directionally until they meet
for i, j in corrupted_bytes:
    uf.add((i, j))
    for delta_i, delta_j in [(-1, 0), (1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1)]:
        new_i, new_j = i + delta_i, j + delta_j
        if (new_i, new_j) in uf:
            uf.union((new_i, new_j), (i, j))
    if i == 0 or j == side_len - 1:
        uf.union(-1, (i, j))
    if j == 0 or i == side_len - 1:
        uf.union(-2, (i, j))
    if uf.connected(-1, -2):
        print(f"{i},{j}")
        break
