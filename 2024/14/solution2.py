import sys
sys.path.append('/'.join(__file__.split("/")[:-3]))
import utils
robots = list(utils.input_lines("p={int},{int} v={int},{int}"))

w, h = 101, 103

def check(cnt):
    possitions = set()
    for x, y, vx, vy in robots:
        x += cnt * vx
        y += cnt * vy

        x = ((x % w) + w) % w
        y = ((y % h) + h) % h

        possitions.add((x, y))

    # I wanna throw up
    passed_test = False
    required_box_side = 3
    for i in range(w - required_box_side + 1):
        for j in range(h - required_box_side + 1):
            fails = False
            for required_x in range(i, i + required_box_side):
                for required_y in range(i, i + required_box_side):
                    if (required_x, required_y) not in possitions:
                        fails = True
                        break
                if fails:
                    break
            if not fails:
                passed_test = True
                break

        if passed_test:
            break
    if not passed_test:
        return

    print(cnt)
    for i in range(w):
        for j in range(h):
            print("#" if  (i, j) in possitions else " ", end = "")
        print(end = "\n")

for i in range(h * w):
    if i % 500 == 0:
        print(100 * i / (h * w), "%")
    check(i)

