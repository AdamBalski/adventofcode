import collections

# dict (of 4 price deltas tuples) -> dict (secret idx -> first num that ends an equivalent delta sequence)
d = collections.defaultdict(lambda: collections.defaultdict(int))

def calc(num, idx):
    prev_num = num
    deltas = []
    for _ in range(2000):
        num ^=  64 * num
        num %= 16777216

        num ^= num // 32
        num %= 16777216

        num ^= 2048 * num
        num %= 16777216
        
        deltas.append((num % 10) - (prev_num % 10))
        while len(deltas) > 4:
            deltas.pop(0)

        if len(deltas) == 4 and idx not in d[tuple(deltas)]:
            d[tuple(deltas)][idx] = num % 10
        prev_num = num

for idx, inn in enumerate(open("/dev/stdin", 'r').read().splitlines()):
    num = calc(int(inn), idx)

print(max(sum(value for value in seq_dict.values()) for seq_dict in d.values()))
