from typing import *
from timer import Timer
import copy
import re
from dataclasses import dataclass, field
import math
from collections import deque, defaultdict

import itertools
import functools


class Rock:
    ROCKS = [
        [(0, 0), (0, 1), (0, 2), (0, 3)],
        [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],
        [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)],
        [(0, 0), (1, 0), (2, 0), (3, 0)],
        [(0, 0), (0, 1), (1, 0), (1, 1)],
    ]

    def __init__(self, pos, t):
        self.pos = pos
        self.pts = self.ROCKS[t%len(self.ROCKS)]
        self.r = max(dx for _, dx in self.pts)
        self.ht = max(dy for dy, _ in self.pts)+1

    def collides(self, M):
        y, x = self.pos
        if y < 0 or x < 0 or x+self.r >= 7:
            return True
        for dy, dx in self.pts:
            if (y+dy, x+dx) in M:
                return True
        return False

    def add(self, M):
        y, x = self.pos
        for dy, dx in self.pts:
            M.add((y+dy, x+dx))


def main():
    infile = "../inputs/" + __file__.replace(".py", ".txt")

    with Timer(f"Reading from {infile}..."):
        with open(infile, "r") as f:
            for line in f.readlines():
                pass
        line = line.strip()
    
    with Timer("part 1"):
        M, h, p = set(), 0, 0
        def drop(t):
            nonlocal h, p
            rock = Rock([h+3, 2], t)
            dirn = 0
            while True:
                if dirn == 1:
                    rock.pos[0] -= 1
                    if rock.collides(M):
                        rock.pos[0] += 1
                        rock.add(M)
                        h = max(h, rock.pos[0]+rock.ht)
                        break
                else:
                    dx = 1 if line[p] == '>' else -1
                    p = (p+1) % len(line)
                    rock.pos[1] += dx
                    if rock.collides(M):
                        rock.pos[1] -= dx
                dirn = 1-dirn

        prev_h, deltas = 0, []
        for t in range(2022):
            drop(t)
            deltas.append(h-prev_h)
            prev_h = h
        
        print("part 1:", h)

    with Timer("part 2"):
        T = 1000000000000
        for t in range(2022, 20000):
            drop(t)
            deltas.append(h-prev_h)
            prev_h = h

        pattern, repeats = [], 0
        for y in range(20, len(deltas)):
            pattern = deltas[-y:]
            end = len(deltas)-len(pattern)
            start = end-len(pattern) 
            repeats = 0
            while start >= 0 and deltas[start:end] == pattern:
                repeats += 1
                start -= len(pattern)
                end -= len(pattern)
            if repeats > 3:
                break
        
        t += 1 # python does not increment this at the end of the loop
        steps = (T-t)//len(pattern)
        t += steps*len(pattern)
        h += steps*sum(pattern)
        for i in range(T-t):
            h += pattern[i]
            
        print("part 2:", h)


if __name__ == '__main__':
    main()
