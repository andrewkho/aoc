from timer import Timer
import re


def main():
    infile = "../inputs/" + __file__.replace(".py", ".txt")

    with Timer(f"Reading from {infile}..."):
        with open(infile, "r") as f:
            lines = f.readlines()

        line = lines[0]

    def solve(line, n) -> int:
        buffer = list(line[:n])
        for i, c in enumerate(line):
            buffer[i%n] = c
            if len(set(buffer)) == n:
                return i+1

    with Timer("part 1"):
        print("part 1:", solve(line, 4))

    with Timer("part 2"):
        print("part 2:", solve(line, 14))


if __name__ == '__main__':
    main()
