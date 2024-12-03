import sys
import collections

left, right = collections.Counter(), collections.Counter()

for line in sys.stdin:
    l, r = [int(number) for number in line.split()]
    left[l] += 1
    right[r] += 1

print(sum(element * count * right[element] for element, count in left.items()))
