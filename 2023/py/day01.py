from timer import Timer
from utils import get_input

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
        for line in lines:
            digits = []
            for c in line:
                if c.isnumeric():
                    digits.append(c)
                    break
            for c in reversed(line):
                if c.isnumeric():
                    digits.append(c)
                    break
            assert len(digits) == 2
            tot += int(''.join(digits))
            
        print("part1:", tot)


    with Timer("part 2"):
        tot = 0
        pattern = r"(?=([1-9]|one|two|three|four|five|six|seven|eight|nine))"
        vals = {
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
            "five": 5,
            "six": 6,
            "seven": 7,
            "eight": 8,
            "nine": 9,
        }
        for line in lines:
            m = re.findall(pattern, line)
            digits = []
            if m[0].isnumeric():
                digits.append(m[0])
            else:
                digits.append(str(vals[m[0]]))

            if m[-1].isnumeric():
                digits.append(m[-1])
            else:
                digits.append(str(vals[m[-1]]))
            assert len(digits) == 2
            tot += int(''.join(digits))
        print("part 2:", tot)


if __name__ == '__main__':
    main()
