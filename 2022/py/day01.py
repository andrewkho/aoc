from timer import Timer


def main():
    infile = "../inputs/" + __file__.replace(".py", ".txt")
    with Timer(f"Reading from {infile}..."):
        with open(infile, "r") as f:
            lines = []
            for line in f.readlines():
                lines.append(line.strip())

    with Timer("part 1"):
        elves = []
        tmp = []
        for line in lines:
            if line == "":
                elves.append(sum(int(x) for x in tmp))
                tmp = []
            else:
                tmp.append(line)
        result = sorted(enumerate(elves), key=lambda x: -x[1])[0]
        print("part1:", result)

    with Timer("part 2"):
        result = sum(y[1] for y in sorted(enumerate(elves), key=lambda x: -x[1])[:3])
        print("part 2:", result)


if __name__ == '__main__':
    main()
