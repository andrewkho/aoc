from timer import Timer
import re
from dataclasses import dataclass, field


def main():
    infile = "../inputs/" + __file__.replace(".py", ".txt")

    with Timer(f"Reading from {infile}..."):
        with open(infile, "r") as f:
            lines = [line.strip() for line in f.readlines()]
        H = len(lines)
        W = len(lines[0])

    with Timer("part 1"):
        seen = set()
        def step(stack, i, j):
            if stack and stack[-1][0] == '9':
                return True
            if not stack or lines[j][i] > stack[-1][0]:
                stack.append((lines[j][i], j))
                seen.add((j, i))
            return False
            
        for i in range(W):
            for rr in [range(H), range(H-1, -1, -1)]:
                stack = []
                for j in rr:
                    if step(stack, i, j):
                        break

        for j in range(H):
            for rr in [range(W), range(W-1, -1, -1)]:
                stack = []
                for i in rr:
                    if step(stack, i, j):
                        break

        print("part 1:", len(seen))

    with Timer("part 2"):
        totals = [[1]*W for _ in range(H)]

        for j in range(H):
            # left to right
            stack = []
            for i in range(W):
                while len(stack) and lines[j][i] > stack[-1][0]:
                    stack.pop()
                if len(stack) == 0:
                    v = i
                else:
                    v = i-stack[-1][1]
                totals[j][i] *= v
                stack.append((lines[j][i], i))

            # right to left
            stack = []
            for i in range(W-1, -1, -1):
                while len(stack) and lines[j][i] > stack[-1][0]:
                    stack.pop()
                if len(stack) == 0:
                    v = W - 1 - i
                else:
                    v = stack[-1][1] - i 
                totals[j][i] *= v
                stack.append((lines[j][i], i))
        
        for i in range(W):
            # up to down
            stack = []
            for j in range(H):
                while len(stack) and lines[j][i] > stack[-1][0]:
                    stack.pop()
                if len(stack) == 0:
                    v = j
                else:
                    v = j-stack[-1][1]
                totals[j][i] *= v
                stack.append((lines[j][i], j))

            # down to up
            stack = []
            for j in range(H-1, -1, -1):
                while len(stack) and lines[j][i] > stack[-1][0]:
                    stack.pop()
                if len(stack) == 0:
                    v = H-1-j
                else:
                    v = stack[-1][1] - j
                totals[j][i] *= v
                stack.append((lines[j][i], j))

        best = max(max(x for x in line) for line in totals)
        print("part 2:", best)


if __name__ == '__main__':
    main()
