from timer import Timer
from utils import get_input, Grid
from collections import defaultdict, Counter
import itertools
import bisect
import math

import re


def main():
    infile = get_input(__file__)
    with Timer(f"Reading from {infile}..."):
        with open(infile, "r") as f:
            lines = []
            for line in f.readlines():
                lines.append(line.strip())

    def get_wins(t, record):
        # t_win^2 - t*t_win + record < 0
        t_win = math.ceil((t - math.sqrt(t*t - 4*record)) / 2)
        if t_win <= 0:
            return 0
        # number of discrete times between t_win, (t-t_win)
        return (t-t_win) - t_win + 1
        
    with Timer("part 1"):
        times = [int(x) for x in lines[0].split(":")[1].split(" ") if x]
        distances = [int(x) for x in lines[1].split(":")[1].split(" ") if x]

        wins = [0]*len(times)
        for i in range(len(times)):
            t, record = times[i], distances[i]
            wins[i] += get_wins(t, record)

        result = 1
        for w in wins:
            result *= w

        print("part1:", result, wins)

    with Timer("part 2"):
        t = int(''.join(x for x in lines[0].split(":")[1].split(" ") if x))
        record = int(''.join(x for x in lines[1].split(":")[1].split(" ") if x))
        result = get_wins(t, record)
        print("part 2:", result)


if __name__ == '__main__':
    main()

