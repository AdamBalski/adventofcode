line = open("/dev/stdin", "r").read().rstrip()

# Move from notation 23245 to [(0, 2), ('.', 3), (1, 2), ('.', 4), (2, 5)]
def convert_to_relaxed(line):
    res = []
    i = 0
    while i < len(line):
        res.append([i // 2, int(line[i])])
        if i + 1 < len(line):
            res.append(['.', int(line[i + 1])])
        i += 2
    return res

def check_sum(line):
    result = 0
    p = 0
    idx = 0
    while p < len(line):
        if line[p][0] != '.':
            for _ in range(line[p][1]):
                result += idx * line[p][0]
                idx += 1
        else:
            idx += line[p][1]
        p += 1
    return result

def make_data_compact(data):
    for i in range(data[-1][0], -1, -1):
        # idx <- i'th file idx
        idx = next(idx for idx, el in enumerate(data) if el[0] == i)
        for j in range(idx):
            # j <- idx of the first space that can fit the i'th file
            if data[j][0] == '.' and data[j][1] >= data[idx][1]:
                data[j][1] -= data[idx][1]
                data.insert(j, list(data[idx]))
                data[idx + 1][0] = '.'
                break
    return data

print(check_sum(make_data_compact(convert_to_relaxed(line))))
