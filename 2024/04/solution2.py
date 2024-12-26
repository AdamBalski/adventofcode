lines = open("/dev/stdin", "r").readlines()

result = 0
for i in range(2, len(lines)):
    for j in range(2, len(lines[0])):
        scan = ''.join([lines[i - 2][j - 2], lines[i - 2][j], lines[i][j - 2], lines[i][j], lines[i - 1][j - 1]])
        if scan in {"MSMSA", "SMSMA", "MMSSA", "SSMMA"}:
            result += 1

print(result)

