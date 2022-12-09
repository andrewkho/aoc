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
            j = 0
            stack = []
            while j < H and not step(stack, i, j):
                j+=1
            j = H-1
            stack = []
            while j >= 0 and not step(stack, i, j):
                j-=1

        for j in range(H):
            i = 0
            stack = []
            while i < W and not step(stack, i, j):
                i += 1
            i = H-1
            stack = []
            while i >= 0 and not step(stack, i, j):
                i -= 1

        print("part 1:", len(seen))

    with Timer("part 2"):
        totals = [[1]*W for _ in range(H)]

        # Single pass with monostack
        for j in range(H):
            stack = []
            for i in range(W):
                h = lines[j][i]
                prev = h
                while stack and h > stack[-1][0]:
                    if stack[-1][0] > prev:
                        totals[j][stack[-1][1]] *= i-stack[-1][1]
                    prev = stack.pop()[0]
                
                totals[j][i] *= i-stack[-1][1] if stack else i

                while stack and h == stack[-1][0]:
                    if stack[-1][0] > prev:
                        totals[j][stack[-1][1]] *= i-stack[-1][1]
                    prev = stack.pop()[0]

                stack.append((h, i))
            
            prev = stack.pop()[0]
            while stack:
                if stack[-1][0] > prev:
                    totals[j][stack[-1][1]] *= W-1 - stack[-1][1]
                prev = stack.pop()[0]
        
        for i in range(W):
            stack = []
            for j in range(H):
                h = lines[j][i]
                prev = h
                while len(stack) and h > stack[-1][0]:
                    if stack[-1][0] > prev:
                        totals[stack[-1][1]][i] *= j-stack[-1][1]
                    prev = stack.pop()[0]
                    
                totals[j][i] *= j-stack[-1][1] if stack else j

                while len(stack) and h == stack[-1][0]:
                    if stack[-1][0] > prev:
                        totals[stack[-1][1]][i] *= j-stack[-1][1]
                    prev = stack.pop()[0]
                stack.append((h, j))
            
            prev = stack.pop()[0]
            while stack:
                if stack[-1][0] > prev:
                    totals[stack[-1][1]][i] *= H-1 - stack[-1][1]
                prev = stack.pop()[0]

        best = max(max(x for x in line) for line in totals)
        print("part 2:", best)


if __name__ == '__main__':
    main()
