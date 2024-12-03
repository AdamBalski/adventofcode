import sys

def same_sign(num1, num2):
    if num1 > 0:
        return num2 > 0
    if num1 < 0:
        return num2 < 0
    return num2 == 0

def is_safe(report):
    first_diff = report[1] - report[0]
    for i in range(len(report) - 1):
        if report[i] == report[i + 1]:
            return False
        if abs(report[i + 1] - report[i]) >= 4:
            return False
        if not same_sign(report[i + 1] - report[i], first_diff):
            return False
    return True

res = 0
for line in sys.stdin:
    curr_nums = [int(num) for num in line.split()]
    if is_safe(curr_nums):
        res += 1

print(res)
