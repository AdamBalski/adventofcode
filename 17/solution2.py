import sys
import matplotlib.pyplot as plt
sys.path.append('/'.join(__file__.split("/")[:-2]))
import utils

DEBUG = False

class Computer:
    def __init__(self, a, b, c, program):
        self.program = program
        self.abc = [a, b, c]
        self.ptr = 0
        self.output = []
        self.ops = [self.__adv, self.__bxl, self.__bst, self.__jnz, self.__bxc, self.__out, self.__bdv, self.__cdv]
        self.txt = ["adv", "bxl", "bst", "jnz", "bxc", "out", "bdv", "cdv"]
    def __combo(self, operand):
        if 0 <= operand <= 3:
            return operand
        if 4 <= operand <= 6:
            return self.abc[operand - 4]
        assert operand != 7
        assert False
    def run(self):
        while self.ptr < len(self.program) and self.ptr >= 0:
            if DEBUG:
                print(f"a, b, c: {self.abc}, ptr: {self.ptr}, {self.txt[self.program[self.ptr]]} {self.program[self.ptr + 1]}")
            self.__op(*self.program[self.ptr:self.ptr + 2])
            self.ptr += 2
    def __op(self, opcode, operand):
        self.ops[opcode](operand)
    def __adv(self, operand):
        self.abc[0] = self.abc[0] // (2 ** self.__combo(operand))
    def __bxl(self, operand):
        self.abc[1] ^= operand
    def __bst(self, operand):
        self.abc[1] = self.__combo(operand) % 8
    def __jnz(self, operand):
        if self.abc[0] == 0:
            return
        # undershoot by 2, so that increase of prog. ptr in __op will get neutralized
        self.ptr = operand - 2
    def __bxc(self, operand):
        self.abc[1] ^= self.abc[2]
    def __out(self, operand):
        self.output.append(self.__combo(operand) % 8)
    def __bdv(self, operand):
        self.abc[1] = self.abc[0] // (2 ** self.__combo(operand))
    def __cdv(self, operand):
        self.abc[2] = self.abc[0] // (2 ** self.__combo(operand))
    def flush(self):
        print("Out:", ','.join(str(el) for el in self.output))

prog = [
        "Register A: {int}",
        "Register B: {int}",
        "Register C: {int}",
        "",
        "Program: {csplit:*int}"
        ]
xs = []
ys = []
pr = list(utils.input_blocks(*prog, filename="./input"))[0]
a, b, c, program = pr
# i = 37404343444734
# while True:
#     i = int(i)
#     print(i)
#     computer = Computer(i, b, c, program)
#     computer.run()
#     xs.append(i)
#     ys.append(int(''.join(str(el) for el in computer.output)))
#     if len(program) - len(computer.output) >= 3:
#         i *= 10
#         continue
#     if len(program) - len(computer.output) >= 1:
#         i *= 1.1
#         continue
#     output = int(''.join(str(el) for el in computer.output))
#     proint = int(''.join(str(el) for el in program))
#     if proint / output >= 1.1:
#         i *= 1.0005
#         continue
#     if proint / output >= 1.001:
#         i *= 1.00005
#         continue
#     break

# 2.
def rep(out):
    res = 0
    for el in out:
        res += 1 + el
        res *= 11
    return res

def rep(out):
    res = 0
    for el in out:
        res += el
        res *= 8
    return res

def rep(out):
    res = 0
    for el in reversed(out):
        res += el + 1
        res *= 9
    return res
i = 37404343444734
i = 37404335151036
i = 37404333480000
i = 37404330200000
reppr = rep(program)
impo = []
output = 0
proint = int(''.join(str(el) for el in program))
for line in []:#sys.stdin:
    a = int(line.rstrip())
    computer = Computer(a, b, c, program)
    computer.run()
    output = computer.output
    o = rep(output)
    if o == reppr:
        print(a, output)
        break
    print(o, "<" if o < proint else ">", proint)
    impo = [a, b, c]
    i -= 1
    print(a, output)
    if i % 10000 == 0: 
        print(i)
#up =37404344890884
print(impo)


# 3.

#i_s = 107416620000000
#i_e = 107516660000000
i_s = 2 ** 45
i_e = 2 ** 48
i_s = 105000000000000
i_e = 142000000000000
i_s = 107413700000000
i_e = 107413708000000
#i_s = 107413680000000
#i_e = 107413898110000
#i_s = int(1.074137e14 + 0e6)
#i_e = int(1.074137e14 + 8e6)
i = i_s
while i < i_e:
    i = int(i)
    computer = Computer(i, b, c, program)
    computer.run()
    xs.append(i)
    ys.append(rep(computer.output))
    o = rep(computer.output)
    #print(i, o, "<" if o < reppr else ">", reppr)
    if reppr == o:
        print(i, "nice:)")
        break
    i += 1#(i_e - i_s) // 120000
    if i % 10000 == 0:
        print(100 * (i-i_s) / (i_e-i_s), "%")

plt.plot(xs, ys)
plt.plot(xs, [rep(program)] * len(xs))
plt.show()

i = i_s
out = []
while rep(out) != reppr:
    computer = Computer(i, b, c, program)
    computer.run()
    out = computer.output
    if i % 10000 == 0:
        print(i)
    i += 1
print(i, "done:)") 

