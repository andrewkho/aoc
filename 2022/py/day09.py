from timer import Timer
import re
from dataclasses import dataclass, field
import math


def main():
    infile = "../inputs/" + __file__.replace(".py", ".txt")

    with Timer(f"Reading from {infile}..."):
        instrs = []
        with open(infile, "r") as f:
            for line in f.readlines():
                d = line[0]
                n = int(line[2:].strip())
                instrs.append((d, n))

    def step(H, T):
        tx, ty = H[0]-T[0], H[1]-T[1]

        # diag
        if abs(tx) > 0 and abs(ty) > 0:
            if abs(tx) > 1 or abs(ty) > 1:
                T[0] += math.copysign(1, tx)
                T[1] += math.copysign(1, ty)
        elif abs(tx) > 1:
            T[0] += math.copysign(1, tx)
        elif abs(ty) > 1:
            T[1] += math.copysign(1, ty)

    DX = {
        'U': [1, 0],
        'D': [-1, 0],
        'L': [0, -1],
        'R': [0, 1],
    }

    with Timer("part 1"):
        T = [0, 0]
        H = [0, 0]
        seen = {(0, 0)}
        for d, n in instrs:
            dx = DX[d]
            for _ in range(n):
                H[0] += dx[0]
                H[1] += dx[1]
                step(H, T)
                seen.add(tuple(T))

        print("part 1:", len(seen))

    with Timer("part 2"):
        rope = [[0, 0] for _ in range(10)]
        seen = {(0, 0)}
        for d, n in instrs:
            dx = DX[d]
            for _ in range(n):
                H = rope[0]
                H[0] += dx[0]
                H[1] += dx[1]
                for T in rope[1:]:
                    prev = tuple(T)
                    step(H, T)
                    if tuple(T) == prev:
                        break
                    H = T
                seen.add(tuple(rope[-1]))
        print("part 2:", len(seen))


if __name__ == '__main__':
    main()
