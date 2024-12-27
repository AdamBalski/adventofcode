from typing import Iterable
from typing import List

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
        self.instructions = {1: self.__add, 2: self.__mul, 3: self.__ass, 4: self.__out, 99: self.__halt}
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
        self.instructions[op % 100](modes)

    # opcode 1
    def __add(self, modes):
        params = self.__get_params(3, modes)
        params[2].write(params[0].read() + params[1].read())
        self.ptr_pos += 4

    # opcode 2
    def __mul(self, modes):
        params = self.__get_params(3, modes)
        params[2].write(params[0].read() * params[1].read())
        self.ptr_pos += 4

    # opcode 3
    def __ass(self, modes):
        params = self.__get_params(2, modes)
        params[0].write(self.next_input())
        self.ptr_pos += 2

    # opcode 4
    def __out(self, modes):
        params = self.__get_params(1, modes)
        self.output.append(params[0].read())
        self.ptr_pos += 2

    # opcode 99
    def __halt(self, modes):
        _ = modes
        self.runs = False

    def next_input(self):
        self.input_ptr += 1
        return self.input[self.input_ptr]


computer = IntCodeInterpreter(map(int, open("/dev/stdin", "r").read().rstrip().split(",")), [1])
computer.run()
print(computer.output_dump())

