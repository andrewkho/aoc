from timer import Timer
from utils import get_input
from collections import defaultdict, Counter

import re


def main():
    infile = get_input(__file__)
    with Timer(f"Reading from {infile}..."):
        with open(infile, "r") as f:
            lines = []
            for line in f.readlines():
                lines.append(line.strip())

    with Timer("part 1"):
        tot = 0
        maxes = {
            "red": 12,
            "green": 13,
            "blue": 14,
        }
        pattern = r"([0-9]+) (blue|red|green)"
        for i, line in enumerate(lines):
            line = line.split(":")[1].strip()
            possible = True
            for game in line.split(";"):
                m = re.findall(pattern, game)
                for match in m:
                    v = int(match[0])
                    c = match[1]
                    if maxes[c] < v:
                        possible = False
                    
            if possible:
                tot += (i+1)

        print("part1:", tot)

    with Timer("part 2"):
        tot = 0
        most = defaultdict(int)
        for line in lines:
            line = line.split(":")[1].strip()
            mins = {"red": 0, "green": 0, "blue": 0}
            for game in line.split(";"):
                m = re.findall(pattern, game)
                for match in m:
                    v = int(match[0])
                    c = match[1]
                    mins[c] = max(mins[c], v)
            
            prod = 1
            for v in mins.values():
                prod *= v
            tot += prod
        print("part 2:", tot)


if __name__ == '__main__':
    main()
