from timer import Timer


def main():
    infile = "../inputs/" + __file__.replace(".py", ".txt")
    with Timer(f"Reading from {infile}..."):
        with open(infile, "r") as f:
            lines = []
            for line in f.readlines():
                lines.append(line.strip())

    def get_score(c: str) -> int:
        if c >= "a":
            return ord(c) - ord('a') + 1
        else:
            return 26 + ord(c) - ord('A') + 1

    with Timer("part 1"):
        score = 0
        for i, line in enumerate(lines):
            n = len(line)
            assert n % 2 == 0
            common = set(line[:n//2]).intersection(set(line[n//2:]))
            for c in common:
                score += get_score(c)
        print("part 1:", score) 

    with Timer("part 2"):
        score = 0
        score = 0
        for i in range(0, len(lines), 3):
            common = set(lines[i]).intersection(lines[i+1]).intersection(lines[i+2])
            for c in common:
                score += get_score(c)
        print("part 2:", score)


if __name__ == '__main__':
    main()
