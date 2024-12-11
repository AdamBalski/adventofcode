import math
import collections

nums = [int(num) for num in open("/dev/stdin", "r").read().splitlines()[0].split()]

def even_digits_count(num):
    return int(math.log10(num)) & 1

def blink(cnts):
    new_data = collections.defaultdict(int)

    for num, cnt in cnts.items():
        if num == 0:
            new_data[1] += cnt
        elif even_digits_count(num):
            digits_one_part = (int(math.log10(num)) + 1) // 2
            b = num % (10 ** digits_one_part)
            a = (num - b) // (10 ** digits_one_part)
            new_data[a] += cnt
            new_data[b] += cnt
        else:
            new_data[num * 2024] += cnt
    return new_data


cnts = collections.defaultdict(int)
for num in nums:
    cnts[num] += 1

for i in range(75):
    cnts = blink(cnts)
print(sum(cnt for _, cnt in cnts.items()))
