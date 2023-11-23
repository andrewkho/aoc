from timer import Timer
from utils import get_input


def main():
    infile = get_input(__file__)
    with Timer(f"Reading from {infile}..."):
        with open(infile, "r") as f:
            lines = []
            for line in f.readlines():
                lines.append(line.strip())

    with Timer("part 1"):
        pass
        # print("part1:", result)

    with Timer("part 2"):
        pass
        # print("part 2:", result)


if __name__ == '__main__':
    main()
