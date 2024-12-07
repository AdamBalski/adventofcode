import sys
import functools

def can_be_made_correct(output, inputs):
    @functools.cache
    def cachable(acc, start):
        if start == len(inputs):
            return output == acc
        return cachable(acc * inputs[start], start + 1) or cachable(acc + inputs[start], start + 1)
    
    return cachable(inputs[0], 1)


result = 0
for line in sys.stdin:
    line_out, line_in = line.split(":")
    line_out = int(line_out)
    line_in = [int(num) for num in line_in.rstrip().split()]
    if can_be_made_correct(line_out, line_in):
        result += line_out
print(result)
