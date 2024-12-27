from typing import Iterable
from typing import List
import collections
from enum import Enum

class ParameterMode(Enum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2
    
class Parameter:
    def __init__(self, computer, mode, value):
        self.computer = computer
        self.mode = mode
        self.value = value
    def write(self, value):
        if self.mode == ParameterMode.IMMEDIATE:
            raise Exception("Cannot write to a parameter with an immediate mode")
        if self.mode == ParameterMode.RELATIVE:
            self.computer[self.computer.get_relative_base() + self.value] = value
            return
        self.computer[self.value] = value
    def read(self):
        if self.mode == ParameterMode.IMMEDIATE:
            return self.value
        if self.mode == ParameterMode.RELATIVE:
            return self.computer[self.computer.get_relative_base() + self.value]
        return self.computer[self.value]

class IntCodeInterpreter:
    def __init__(self, data: Iterable[int], input_list):
        self.ptr_pos = 0
        self.data = list(data)
        self.sparse_memtable = collections.defaultdict(int)
        self.runs = True
        self.stalled = False
        self.instructions = [self.__add, self.__multiply, self.__assignment, self.__output, \
                self.__jump_if_true, self.__jump_if_false, self.__less_than, self.__equals, \
                self.__change_relative_base]
        self.output = []
        self.input = input_list
        self.input_ptr = -1
        self.curr_relative_base = 0

    def __getitem__(self, idx):
        if idx >= len(self.data):
            return self.sparse_memtable[idx]
        return self.data[idx]

    def __setitem__(self, idx, val):
        if idx >= len(self.data):
            self.sparse_memtable[idx] = val
            return
        self.data[idx] = val

    def get_relative_base(self):
        return self.curr_relative_base

    def push_input(self, *vals):
        self.input.extend(vals)
        if self.runs:
            self.run()

    def data_dump(self):
        return self.data

    def output_flush(self):
        res = self.output
        self.output = []
        return res

    def output_dump(self):
        return self.output

    def run(self):
        while self.runs:
            self.__run_once()
            if self.stalled:
                break

    def __get_params(self, count, modes) -> List[Parameter]:
        params = []
        idx = 0
        
        while idx < count:
            curr = self[self.ptr_pos + 1 + idx]
            if modes % 10 == 0:
                params.append(Parameter(self, ParameterMode.POSITION, curr))
            elif modes % 10 == 1:
                params.append(Parameter(self, ParameterMode.IMMEDIATE, curr))
            elif modes % 10 == 2:
                params.append(Parameter(self, ParameterMode.RELATIVE, curr))
            else:
                raise Exception(f"Invalid parameter mode: {modes % 10}")
            modes //= 10
            idx += 1
        return params

    def __run_once(self):
        if not self.runs:
            return
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
        if not self.next_input_exists():
            self.stalled = True
            return
        self.stalled = False
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

    # opcode 9
    def __change_relative_base(self, modes):
        params = self.__get_params(1, modes)
        self.curr_relative_base += params[0].read()
        self.ptr_pos += len(params) + 1

    # opcode 99
    def __halt(self, modes):
        _ = modes
        self.runs = False
    
    def next_input_exists(self):
        return self.input_ptr + 1 < len(self.input)

    def next_input(self):
        self.input_ptr += 1
        return self.input[self.input_ptr]

program = [int(code) for code in open("/dev/stdin", "r").read().rstrip().split(",")]
vm = IntCodeInterpreter(program, [])

# hull colours data
hull = collections.defaultdict(int)
coloured = set()
# robot data
position = (0, 0)
directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
dir_idx = 2
while vm.runs:
    vm.push_input(hull[position])
    paint_num, turn_num = vm.output_flush()

    hull[position] = paint_num
    coloured.add(position)
    dir_idx = (dir_idx + (1 if turn_num == 1 else -1) + 4) % 4
    position = tuple(position[i] + directions[dir_idx][i] for i in range(2))

print(len(coloured))
