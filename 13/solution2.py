import sys

# Solves for (a, b) such that: 
#     a * a_x + b * b_x = x 
# and a * a_y + b * b_y = y
def tokens(a_x, a_y, b_x, b_y, x, y):
    x += 10000000000000
    y += 10000000000000

    # check that determinant is nonzero
    assert a_x * b_y - b_x * a_y != 0
    b = (y * a_x - a_y * x) / (b_y * a_x - b_x * a_y)
    a = (x - b_x * b) / a_x
    if int(a) != a or int(b) != b:
        return 0
    return 3 * a + b

result = 0
for line in sys.stdin:
    line = [int(num) for num in line.replace("Button A: X+", "").replace(", Y+", " ").replace("Button B: X+", " ").replace(" Prize: X=", " ").replace(", Y=", " ").rstrip().split()]
    result += tokens(*line)
print(result)


