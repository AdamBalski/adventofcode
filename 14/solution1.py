import sys
sys.path.append('/'.join(__file__.split("/")[:-2]))
import utils

w, h = 101, 103
qw, qh = w // 2, h // 2

quads = [0] * 4
for x, y, vx, vy in utils.input_lines("p={int},{int} v={int},{int}"):
    x += 100 * vx
    y += 100 * vy

    x = ((x % w) + w) % w
    y = ((y % h) + h) % h

    if x == qw or y == qh:
        continue

    lr = 1 if x < qw else 0
    tb = 1 if y < qh else 0
    quad = 2 * lr + tb
    quads[quad] += 1

res = 1
for quad in quads:
    res *= quad
print(res)
