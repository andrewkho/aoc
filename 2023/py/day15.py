import multiprocessing as mp
from typing import *
from timer import Timer
import utils
from utils import get_input, Grid
from collections import defaultdict, Counter, deque
import itertools
import bisect
import functools
import copy

import re


class HM:
    def __init__(self, size=256):
        self.size = 256
        self.arr = [deque() for _ in range(self.size)]

    def hash_fn(self, s: str):
        v = 0
        for c in s:
            v += ord(c)
            v *= 17
            v %= self.size
        return v

    def __setitem__(self, k: str, v: int):
        b = self.hash_fn(k)
        done = False
        for i in range(len(self.arr[b])):
            if self.arr[b][i][0] == k:
                self.arr[b][i][1] = v
                done = True
                return
        if not done:
            self.arr[b].append([k, v])
    
    def __delitem__(self, k: str):
        b = self.hash_fn(k)
        for i in range(len(self.arr[b])):
            if self.arr[b][i][0] == k:
                del self.arr[b][i]
                return

def main():
    infile = get_input(__file__)
    with Timer(f"Reading from {infile}..."):
        with open(infile, "r") as f:
            lines = []
            for line in f.readlines():
                lines.append(line.strip())
    
    hm = HM()
    with Timer("part 1"):
        line = lines[0]

        result = 0
        for s in line.split(","):
            result += hm.hash_fn(s)
        print("part1:", result)

    with Timer("part 2"):
        hm = HM()

        for s in line.split(","):
            if "=" in s:
                k, v = s.split("=")
                hm[k] = int(v)
            elif "-" in s:
                k = s.split("-")[0]
                del hm[k]

        result = 0
        for i, dq in enumerate(hm.arr):
            for j, (k, v) in enumerate(dq):
                result += (i+1)*(j+1)*v
        print("part 2:", result)


if __name__ == '__main__':
    main()
