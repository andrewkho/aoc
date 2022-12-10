from timer import Timer
import re
from dataclasses import dataclass, field
import math
from collections import deque


def main():
    infile = "../inputs/" + __file__.replace(".py", ".txt")

    with Timer(f"Reading from {infile}..."):
        instrs = []
        with open(infile, "r") as f:
            for line in f.readlines():
                x = line.strip().split(' ')
                if len(x) == 1:
                    instrs.append((x[0], ))
                else:
                    instrs.append((x[0], int(x[1])))

    with Timer("part 1"):
        q = deque([20, 60, 100, 140, 180, 220])
        i, X = 1, 1
        screen = []
        results = []

        def crt(i, X):
            row, col = (i-1)//40, (i-1)%40
            while row >= len(screen):
                screen.append([" "]*40)
            if abs(col-X) <= 1:
                screen[row][col] = '#'

        for instr in instrs:
            if instr[0] == "noop":
                crt(i, X)
                i += 1
                if q and i > q[0]:
                    results.append(X*q.popleft())
            else:
                crt(i, X)
                i += 1
                crt(i, X)
                i += 1
                if q and i > q[0]:
                    results.append(X*q.popleft())
                X += instr[1]
            
        print("part 1:", sum(results))

    with Timer("part 2"):
        print("part 2:")
        for line in screen:
            print(''.join(line))


if __name__ == '__main__':
    main()
