import sys
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
        self.flush()
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
for a, b, c, program in utils.input_blocks(*prog):
    print(a, b, c, program)
    computer = Computer(a, b, c, program)
    computer.run()

