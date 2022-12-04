from timer import Timer


def main():
    infile = "../inputs/" + __file__.replace(".py", ".txt")
    with Timer(f"Reading from {infile}..."):
        with open(infile, "r") as f:
            lines = []
            for line in f.readlines():
                lines.append(line.strip())

    with Timer("part 1"):
        total = 0
        total2 = 0
        for i, line in enumerate(lines):
            left, right = line.split(",")
            left = [int(x) for x in left.split("-")]
            right = [int(x) for x in right.split("-")]

            if left[0] >= right[0] and left[1] <= right[1]:
                total += 1
            elif left[0] <= right[0] and left[1] >= right[1]:
                total += 1
            elif left[0] <= right[0] <= left[1]:
                total2 += 1
            elif right[0] <= left[0] <= right[1]:
                total2 += 1
        print("part 1:", total) 

    with Timer("part 2"):
        print("part 2:", total+total2)


if __name__ == '__main__':
    main()
