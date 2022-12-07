from timer import Timer
import re
from dataclasses import dataclass, field


@dataclass
class Dir:
    name: str
    children: dict = field(default_factory=dict)


@dataclass
class File:
    size: int
    

def main():
    infile = "../inputs/" + __file__.replace(".py", ".txt")

    root = Dir("/")
    root.children[".."] = root
    cur = root
    with Timer(f"Reading from {infile}..."):
        with open(infile, "r") as f:
            for line in f.readlines():
                token = line.strip().split(" ")
                if token[0] == '$':
                    if token[1] == "cd":
                        name = token[2]
                        if name == "/":
                            cur = root
                        else:
                            cur = cur.children[name]
                    elif token[1] == "ls":
                        continue
                    else:
                        raise ValueError(token[1])
                elif token[0] == 'dir':
                    name = token[1]
                    cur.children[name] = Dir(cur.name + "/" + name, {"..": cur})
                elif token[0].isnumeric():
                    name = token[1]
                    cur.children[name] = File(int(token[0]))
                else:
                    raise ValueError(token[0])

    with Timer("part 1"):
        results = {}
        def get_size(node) -> int:
            if isinstance(node, File):
                return node.size

            total = sum(get_size(child) 
                        for name, child in node.children.items() 
                        if name != "..")
            results[node.name] = total
            return total

        get_size(root)
        print("part 1:", sum(x for x in results.values() if x <= 100000))

    with Timer("part 2"):
        minimum = 30000000 - (70000000 - results["/"])
        best = 30000000
        for v in results.values():
            if v >= minimum and v < best:
                best = v
        print("part 2:", best)


if __name__ == '__main__':
    main()
