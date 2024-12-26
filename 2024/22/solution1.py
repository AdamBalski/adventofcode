def calc(num):
    for _ in range(2000):
        num ^=  64 * num
        num %= 16777216

        num ^= num // 32
        num %= 16777216

        num ^= 2048 * num
        num %= 16777216
    return num

print(sum(calc(int(num_str)) for num_str in open("/dev/stdin", 'r').read().splitlines()))
