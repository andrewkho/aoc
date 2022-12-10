from timer import Timer
import re
from dataclasses import dataclass, field


def main():
    infile = "../inputs/" + __file__.replace(".py", ".txt")

    with Timer(f"Reading from {infile}..."):
        with open(infile, "r") as f:
            lines = [list(map(int, line.strip())) for line in f.readlines()]
        H = len(lines)
        W = len(lines[0])

    with Timer("part 1"):
        seen = set()
        def step(stack, i, j):
            if not stack or lines[j][i] > stack[-1][0]:
                stack.append((lines[j][i], j))
                seen.add((j, i))
            
        for i in range(W):
            stack1, stack2 = [], []
            for j in range(H):
                step(stack1, i, j)
                step(stack2, i, H-1-j)

        for j in range(H):
            stack1, stack2 = [], []
            for i in range(W):
                step(stack1, i, j)
                step(stack2, W-1-i, j)

        print("part 1:", len(seen))

    with Timer("part 2"):
        # Single pass with monostack, == case is tricky
        totals = [[1]*W for _ in range(H)]
        for j in range(H):
            stack = []
            for i in range(W):
                h = lines[j][i]
                prev = h, 0
                while stack and h >= stack[-1][0]:
                    totals[j][stack[-1][1]] *= i-stack[-1][1]
                    prev = stack.pop()
                totals[j][i] *= i-prev[1] if prev[0] == h else i-stack[-1][1] if stack else i
                stack.append((h, i))
            
            while stack:
                totals[j][stack[-1][1]] *= W-1 - stack[-1][1]
                stack.pop()
        
        for i in range(W):
            stack = []
            for j in range(H):
                h = lines[j][i]
                prev = h, 0
                while stack and h >= stack[-1][0]:
                    totals[stack[-1][1]][i] *= j-stack[-1][1]
                    prev = stack.pop()
                totals[j][i] *= j-prev[1] if prev[0] == h else j-stack[-1][1] if stack else j
                stack.append((h, j))
            
            while stack:
                totals[stack[-1][1]][i] *= H-1 - stack[-1][1]
                stack.pop()

        best = max(max(x for x in line) for line in totals)
        print("part 2:", best)


if __name__ == '__main__':
    main()
