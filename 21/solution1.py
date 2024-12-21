import functools


def log(caption, on=True):
    def decorator(fun):
        if not on:
            return fun
        def wrapped(*args):
            result = fun(*args)
            print(f"{caption}: {args} -> {result}")
            return result
        return wrapped
    return decorator


dir_button_to_pos = {
        '<': (1, 0),
        '>': (1, 2),
        'v': (1, 1),
        '^': (0, 1),
        'A': (0, 2),
}
num_button_to_pos = {
        '1': (2, 0),
        '2': (2, 1),
        '3': (2, 2),
        '4': (1, 0),
        '5': (1, 1),
        '6': (1, 2),
        '7': (0, 0),
        '8': (0, 1),
        '9': (0, 2),
        '0': (3, 1),
        'A': (3, 2),
}
num_pad = ["789", "456", "123", " 0A"]
dir_pad = [" ^A", "<v>"]
dirs = {"v": (1, 0), "^": (-1, 0), ">": (0, 1), "<": (0, -1)}

class Robot:
    def __init__(self, last_button, controller_lvl, out_level):
        if out_level == 3:
            self.states = [(0, 2)] * 2 + [num_button_to_pos[last_button]]
        elif out_level != 0:
            self.states = [(0, 2)] * (out_level - 1) + [dir_button_to_pos[last_button]] + [(0, 2)] * (2 - out_level) + [(3, 2)]
        else:
            self.states = [(0,0)]
        self.controller_lvl = controller_lvl
        self.out_level = out_level
    @log("move", on=False)
    def move(self, c):
        if self.controller_lvl == 3:
            return c
        for i in range(self.controller_lvl, 2):
            if self.out_level == i:
                return c
            # previous interface called to make this interface yield to the next one
            if c == 'A':
                c = dir_pad[self.states[i][0]][self.states[i][1]]
                continue
            # previous interface called to make this robot's arm move
            dirr = dirs[c]
            self.states[i] = (self.states[i][0] + dirr[0], self.states[i][1] + dirr[1])
            # moved to an incorrect place -> halt
            if self.states[i] not in ((0, 1), (0, 2), (1, 0), (1, 1), (1, 2)):
                return False
            # ops should not be flushed after moving an arm
            return True
        if self.out_level != 3:
            return c
        if c == 'A':
            return num_pad[self.states[-1][0]][self.states[-1][1]]
        dirr = dirs[c]
        self.states[-1] = (self.states[-1][0] + dirr[0], self.states[-1][1] + dirr[1])
        return self.states[-1] in {(2, 0), (2, 1), (2, 2), (1, 0), (1, 1),
                                   (1, 2), (0, 0), (0, 1), (0, 2), (3, 1), (3, 2)}
    def move_batch(self, moves):
        result = []
        for cmd in moves:
            curr = self.move(cmd)
            if curr is False:
                return f"halt: {result}"
            if curr is True:
                continue
            result.append(curr)
        return ''.join(result)


def sequence_generator():
    yield ">>^A"
    alphabet = "v<>^A"
    length = 0

    while True:
        for i in range(5 ** length):
            curr = []
            for _ in range(length):
                curr.append(alphabet[i % 5])
                i //= 5
            yield ''.join(curr)
        length += 1
@functools.cache
@log("button cost", on=False)
def button_cost(button_prev, button, controller_lvl, in_level):
    if controller_lvl == in_level:
        return 1
    ans = 1000
    term_when = 20
    for seq in sequence_generator():
        if len(seq) >= term_when:
            return ans

        rbt = Robot(button_prev, controller_lvl - 1, controller_lvl)
        result = 0
        prev = "A"
        for c in seq:
            curr_res = rbt.move(c)
            result += button_cost(prev, c, controller_lvl - 1, in_level)
            prev = c
            if not curr_res:
                break
            if curr_res == button:
                if result < ans:
                    ans = result
                term_when = min(term_when, len(seq) + 2)
                break
            if curr_res is True:
                continue
            break
    return ans

def text_cost(text, controller_level, in_level=0):
    result = 0
    prev = "A"
    for c in text:
        result += button_cost(prev, c, controller_level, in_level)
        prev = c
    return result


def complexity(code):
    return text_cost(code, 3) * int(code[:len(code) - 1])
print(sum((complexity(code) for code in open("/dev/stdin", "r").read().splitlines())))

