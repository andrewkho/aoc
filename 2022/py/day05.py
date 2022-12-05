from timer import Timer
import re


def main():
    infile = "../inputs/" + __file__.replace(".py", ".txt")

    with Timer(f"Reading from {infile}..."):
        stacks = [list() for _ in range(10)]
        instrs = []
        _section1 = True
        matcher = re.compile(r"^move ([0-9]+) from ([0-9]+) to ([0-9]+)$")
        with open(infile, "r") as f:
            lines = f.readlines()

        for line in lines:
            if _section1:
                if line.strip() == "":
                    _section1 = False
                    continue
                for i, stack in enumerate(stacks[1:]):
                    pos = 1 + i*4
                    if len(line) <= pos:
                        break
                    if line[pos] != " ":
                        stack.append(line[pos])
            else:
                m = matcher.match(line.strip())
                groups = m.groups()
                instrs.append((int(groups[0]), int(groups[1]), int(groups[2])))
        stacks = [stack[::-1][1:] for stack in stacks]

    with Timer("Part 1"):
        stacks_orig = [stack.copy() for stack in stacks]

        for n, src, dst in instrs:
            for _ in range(n):
                stacks[dst].append(stacks[src].pop())

        print(''.join(stack[-1] for stack in stacks[1:]) )

    with Timer("Part 2"):
        stacks = stacks_orig
        for n, src, dst in instrs:
            stacks[dst].extend(stacks[src][-n:])
            stacks[src] = stacks[src][:-n]

        print(''.join(stack[-1] for stack in stacks[1:]) )


if __name__ == '__main__':
    main()
