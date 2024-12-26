import sys
import heapq

pq_left, pq_right = [], []

for line in sys.stdin:
    l, r = [int(number) for number in line.split()]
    heapq.heappush(pq_left, l)
    heapq.heappush(pq_right, r)

result = 0
while pq_left:
    result += abs(heapq.heappop(pq_left) - heapq.heappop(pq_right))

print(result)

