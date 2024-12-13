import sys
sys.path.append('/'.join(__file__.split("/")[:-2]))
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

input_format = [
    "Button A: X+{}, Y+{}",
    "Button B: X+{}, Y+{}",
    "Prize: X={}, Y={}"
]
print(sum(tokens(*fields) for fields in utils.input_blocks(*input_format, default_func=int)))
