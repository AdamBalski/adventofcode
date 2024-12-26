lines = open("/dev/stdin", "r").readlines()

result = 0
for i in range(len(lines)):
    for j in range(len(lines[0])):
        candidates = []
        if i >= 3:
            candidates.append([lines[i - delta][j] for delta in range(4)])
        if j >= 3:
            candidates.append([lines[i][j - delta] for delta in range(4)])
        if i >= 3 and j >= 3:
            candidates.append([lines[i - delta][j - delta] for delta in range(4)])
        if i >= 3 and j + 3 < len(lines[0]):
            candidates.append([lines[i - delta][j + delta] for delta in range(4)])
        result += sum(1 for candidate in candidates if ''.join(candidate) in {"XMAS", "SAMX"}) 

print(result)

