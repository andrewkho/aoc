from timer import Timer
import re
from dataclasses import dataclass, field


def main():
    infile = "../inputs/" + __file__.replace(".py", ".txt")

    with Timer(f"Reading from {infile}..."):
        with open(infile, "r") as f:
            lines = [list(map(int, line.strip())) for line in f.readlines()]
        H, W = len(lines), len(lines[0])

    with Timer("part 1"):
        seen = set()
        def step(h, i, j):
            if h < 0 or lines[j][i] > h:
                seen.add((j, i))
                return lines[j][i]
            return h

        for i in range(W):
            h1, h2 = -1, -1
            for j in range(H):
                h1 = step(h1, i, j)
                h2 = step(h2, i, H-1-j)

        for j in range(H):
            h1, h2 = -1, -1
            for i in range(W):
                h1 = step(h1, i, j) 
                h2 = step(h2, W-1-i, j)

        print("part 1:", len(seen))

    with Timer("part 2"):
        # Single pass with monostack, == case is tricky
        totals = [[1]*W for _ in range(H)]
        for j in range(H):
            stack = []
            for i in range(W):
                h = lines[j][i]
                sh, si = h, 0
                while stack and h >= stack[-1][0]:
                    sh, si = stack.pop()
                    totals[j][si] *= i-si
                totals[j][i] *= i-si if sh == h else i-stack[-1][1] if stack else i
                stack.append((h, i))
            
            while stack:
                sh, si = stack.pop()
                totals[j][si] *= W-1 - si
        
        for i in range(W):
            stack = []
            for j in range(H):
                h = lines[j][i]
                sh, sj = h, 0
                while stack and h >= stack[-1][0]:
                    totals[sj][i] *= j-sj
                    sh, sj = stack.pop()
                totals[j][i] *= j-sj if sh == h else j-stack[-1][1] if stack else j
                stack.append((h, j))
            
            while stack:
                sh, sj = stack.pop()
                totals[sj][i] *= H-1 - sj

        best = max(max(x for x in line) for line in totals)
        print("part 2:", best)


if __name__ == '__main__':
    main()
