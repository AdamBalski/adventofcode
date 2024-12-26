from typing import Iterable

class IntCodeInterpreter:
    def __init__(self, data: Iterable[int]):
        self.ptr_pos = 0
        self.data = list(data)
        self.runs = True
        self.opcodes = {1: self.__add, 2: self.__mul, 99: self.__halt}

    def __getitem__(self, idx):
        return self.data[idx]

    def __setitem__(self, idx, val):
        self.data[idx] = val

    def data_dump(self):
        return self.data

    def run(self):
        while self.runs:
            self.__run_once()

    def __run_once(self):
        self.opcodes[self[self.ptr_pos]]()

    # opcode 1
    def __add(self):
        read_idx_1 = self[self.ptr_pos + 1]
        read_idx_2 = self[self.ptr_pos + 2]
        write_idx = self[self.ptr_pos + 3]
        self[write_idx] = self[read_idx_1] + self[read_idx_2]
        self.ptr_pos += 4

    # opcode 2
    def __mul(self):
        read_idx_1 = self[self.ptr_pos + 1]
        read_idx_2 = self[self.ptr_pos + 2]
        write_idx = self[self.ptr_pos + 3]
        self[write_idx] = self[read_idx_1] * self[read_idx_2]
        self.ptr_pos += 4

    # opcode 99
    def __halt(self):
        self.runs = False


init = list(map(int, open("/dev/stdin", "r").read().rstrip().split(",")))
result = -1
for noun in range(100):
    for verb in range(100):
        computer = IntCodeInterpreter(list(init))
        computer[1] = noun
        computer[2] = verb
        computer.run()
        if computer[0] == 19690720:
            result = 100 * noun + verb
            break
if result == -1:
    print("correct noun and verb combination not found:(")
    exit(0)
print(result)
