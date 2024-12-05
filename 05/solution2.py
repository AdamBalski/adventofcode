import sys
import collections

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

needed_by = collections.defaultdict(lambda: [])
for line in sys.stdin:
    line = line.strip()
    if line == "":
        break
    curr = [int(num) for num in line.split("|")]
    needed_by[curr[0]].append(curr[1])

result = 0
for line in sys.stdin:
    curr = [int(num) for num in line.split(",")]

    # connects numbers that are incorrectly placed and related by rules
    uf = UnionFind()

    num_to_idx = {}
    for idx in range(len(curr)):
        num_to_idx[curr[idx]] = idx
        for required_after in needed_by[curr[idx]]:
            if required_after in num_to_idx:
                uf.union(idx, num_to_idx[required_after])

    if len(uf) == 0:
        continue
    if (len(curr) // 2) not in uf:
        result += curr[len(curr) // 2]
        continue

    indices_to_correct = uf.subset(len(curr) // 2)
    bad_ordered_nums = []
    middle_element_idx = -1
    indegree = {}

    indices_to_correct.sort()
    for i, idx_to_correct in enumerate(indices_to_correct):
        bad_ordered_nums.append(curr[idx_to_correct])
        indegree[bad_ordered_nums[-1]] = 0
        if idx_to_correct == len(curr) // 2:
            middle_element_idx = i

    # top sort `bad_ordered_nums` according to `needed_by` and 
    #   add `middle_element_idx`'th element to result
    for num in bad_ordered_nums:
        for dependant in needed_by[num]:
            if dependant not in bad_ordered_nums:
                continue
            indegree[dependant] += 1

    queue = []
    for num, needed in indegree.items():
        if needed == 0:
            queue.append(num)

    topsorted = []
    while queue:
        curr = queue.pop()
        topsorted.append(curr)
        for dependant in needed_by[curr]:
            if dependant in bad_ordered_nums:
                indegree[dependant] -= 1
                if indegree[dependant] == 0:
                    queue.append(dependant)

    result += topsorted[middle_element_idx]

print(result)
