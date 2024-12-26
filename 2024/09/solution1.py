line = open("/dev/stdin", "r").read().rstrip()

# Move from notation 23245 to [(0, 2), ('.', 3), (1, 2), ('.', 4), (2, 5)]
def convert_to_relaxed(line):
    res = []
    i = 0
    while i < len(line):
        for _ in range(int(line[i])):
            res.append(i // 2)
        if i + 1 < len(line):
            for _ in range(int(line[i + 1])):
                res.append('.')
        i += 2
    return res

def check_sum_of_rearranged(line):
    # two pointers:
    # go from left:
    # * when you encounter a dot, then take the next file block
    #       from the right hand side(q pointer), then add its checksum component. 
    #       decrease the right pointer
    # * when you encounter a number then add its component to check sum
    result = 0
    p = 0
    q = len(line) - 1
    idx = 0
    while p <= q:
        if line[p] != '.':
            result += idx * line[p]
            p += 1
            idx += 1
            continue
        result += idx * line[q]
        p += 1
        idx += 1

        q -= 1
        while line[q] == '.' and p <= q:
            q -= 1

    return result

print(check_sum_of_rearranged(convert_to_relaxed(line)))

