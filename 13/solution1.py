import sys
import math
import sys
sys.path.append('/'.join(__file__.split("/")[:-2]))
import utils

def tokens(a_x, a_y, b_x, b_y, x, y):
    def possible_pairs(x, y, a_x, a_y, b_x, b_y):
        max_a = math.ceil(max(x / a_x, y / a_y))
        max_b = math.ceil(max(x / b_x, y / b_y))
        for a in range(max_a + 1):
            for b in range(max_b + 1):
                yield a, b

    tokens = 0

    pairs = possible_pairs(x, y, a_x, a_y, b_x, b_y)
    for a, b in pairs:
        if a * a_x + b * b_x == x and a * a_y + b * b_y == y:
            if tokens == 0:
                tokens = 3 * a + b
            tokens = min(tokens, 3 * a + b)
    return tokens

input_format = [
    "Button A: X+{}, Y+{}",
    "Button B: X+{}, Y+{}",
    "Prize: X={}, Y={}"
]
print(sum(tokens(*fields) for fields in utils.input_blocks(*input_format, default_func=int)))
