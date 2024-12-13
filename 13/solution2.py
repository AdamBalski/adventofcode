import sys
sys.path.append("..")
import utils

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
    return int(3 * a + b)

result = 0
data = utils.input_lines("Button A: X+{}, Y+{}\nButton B: X+{}, Y+{}\nPrize: X={}, Y={}\n")
for extracted_fields in data:
    result += tokens(*(int(field) for field in extracted_fields))
print(result)


