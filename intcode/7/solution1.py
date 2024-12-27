from typing import Iterable
from typing import List
import functools
import operator

class Parameter:
    def __init__(self, computer, is_immediate, value):
        self.computer = computer
        self.is_immediate = is_immediate
        self.value = value
    def write(self, value):
        if self.is_immediate:
            raise Exception("Cannot write to a parameter with an immediate mode")
        self.computer[self.value] = value
    def read(self):
        if self.is_immediate:
            return self.value
        return self.computer[self.value]

class IntCodeInterpreter:
    def __init__(self, data: Iterable[int], input_list):
        self.ptr_pos = 0
        self.data = list(data)
        self.runs = True
        self.instructions = [self.__add, self.__multiply, self.__assignment, self.__output, \
                self.__jump_if_true, self.__jump_if_false, self.__less_than, self.__equals]
        self.output = []
        self.input = input_list
        self.input_ptr = -1

    def __getitem__(self, idx):
        return self.data[idx]

    def __setitem__(self, idx, val):
        self.data[idx] = val

    def data_dump(self):
        return self.data

    def output_dump(self):
        return self.output

    def run(self):
        while self.runs:
            self.__run_once()

    def __get_params(self, count, modes) -> List[Parameter]:
        params = []
        idx = 0
        
        while idx < count:
            curr = self[self.ptr_pos + 1 + idx]
            if modes % 10 == 0:
                params.append(Parameter(self, False, curr))
            elif modes % 10 == 1:
                params.append(Parameter(self, True, curr))
            else:
                raise Exception(f"Invalid parameter mode: {modes % 10}")
            modes //= 10
            idx += 1
        return params

    def __run_once(self):
        op = self[self.ptr_pos]
        modes = op // 100
        if op % 100 == 99:
            self.__halt(modes)
            return
        self.instructions[(op % 100) - 1](modes)

    # opcode 1
    def __add(self, modes):
        params = self.__get_params(3, modes)
        params[2].write(params[0].read() + params[1].read())
        self.ptr_pos += len(params) + 1

    # opcode 2
    def __multiply(self, modes):
        params = self.__get_params(3, modes)
        params[2].write(params[0].read() * params[1].read())
        self.ptr_pos += len(params) + 1

    # opcode 3
    def __assignment(self, modes):
        params = self.__get_params(1, modes)
        params[0].write(self.next_input())
        self.ptr_pos += len(params) + 1

    # opcode 4
    def __output(self, modes):
        params = self.__get_params(1, modes)
        self.output.append(params[0].read())
        self.ptr_pos += len(params) + 1

    # opcode 5
    def __jump_if_true(self, modes):
        params = self.__get_params(2, modes)
        if params[0].read() != 0:
            self.ptr_pos = params[1].read()
            return
        self.ptr_pos += len(params) + 1

    # opcode 6
    def __jump_if_false(self, modes):
        params = self.__get_params(2, modes)
        if params[0].read() == 0:
            self.ptr_pos = params[1].read()
            return
        self.ptr_pos += len(params) + 1

    # opcode 7
    def __less_than(self, modes):
        params = self.__get_params(3, modes)
        is_less_than = params[0].read() < params[1].read()
        params[2].write(1 if is_less_than else 0)
        self.ptr_pos += len(params) + 1
    
    # opcode 8
    def __equals(self, modes):
        params = self.__get_params(3, modes)
        are_equal = params[0].read() == params[1].read()
        params[2].write(1 if are_equal else 0)
        self.ptr_pos += len(params) + 1

    # opcode 99
    def __halt(self, modes):
        _ = modes
        self.runs = False

    def next_input(self):
        self.input_ptr += 1
        return self.input[self.input_ptr]

def ith_permutation(numbers, i):
    copy = list(numbers)
    result = []
    len_minus_1_factorial = functools.reduce(operator.mul, range(1, len(numbers) + 1), 1)
    while copy:
        len_minus_1_factorial //= len(copy)
        result.append(copy.pop(i // len_minus_1_factorial))
        i %= len_minus_1_factorial

    return result


program = [int(code) for code in open("/dev/stdin", "r").read().rstrip().split(",")]
def compute(permutation):
    prev_output = 0
    for phase_setting in permutation:
        computer = IntCodeInterpreter(program, [phase_setting, prev_output])
        computer.run()
        out = computer.output_dump()
        assert len(out) == 1
        prev_output = out[0]
    print(permutation, prev_output)
    return prev_output
print(max(compute(ith_permutation(range(5), i)) for i in range(120)))