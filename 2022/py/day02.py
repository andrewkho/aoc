from timer import Timer


def main():
    infile = "../inputs/" + __file__.replace(".py", ".txt")
    with Timer(f"Reading from {infile}..."):
        with open(infile, "r") as f:
            lines = []
            for line in f.readlines():
                lines.append(line.strip())

    with Timer("part 1"):
        points = {
            "rock": 1,
            "paper": 2,
            "scissors": 3,
        }
        pairs = {
            ("rock", "paper"): 6,
            ("rock", "rock"): 3,
            ("rock", "scissors"): 0,
            ("paper", "rock"): 0,
            ("paper", "paper"): 3,
            ("paper", "scissors"): 6,
            ("scissors", "rock"): 6,
            ("scissors", "scissors"): 3,
            ("scissors", "paper"): 0,
        }
        mapping = {
            "A": "rock",
            "B": "paper",
            "C": "scissors",
            "X": "rock",
            "Y": "paper",
            "Z": "scissors",
        }

        score = 0
        for line in lines:
            p0 = mapping[line[0]]
            p1 = mapping[line[2]]
            score += points[p1] + pairs[p0, p1]
        print("part1:", score)

    with Timer("part 2"):
        score = 0
        mapping = {
            "A": "rock",
            "B": "paper",
            "C": "scissors",
            "X": 0,
            "Y": 3,
            "Z": 6,
        }
        reverse = {
            (p0, outcome): p1
            for (p0, p1), outcome in pairs.items()
        }
        for line in lines:
            p0 = mapping[line[0]]
            outcome = mapping[line[2]]
            score += outcome

            p1 = reverse[p0, outcome]
            score += points[p1]

        print("part 2:", score)


if __name__ == '__main__':
    main()
