# 1.
line = open("/dev/stdin", "r").read().splitlines()
# 2.
import sys

for line in (line.rstrip() for line in sys.stdin):
    pass
