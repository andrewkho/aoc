import fire


def _part_one(vals):
    def iterate():
        for i, a in enumerate(vals):
            for j, b in enumerate(vals[i+1:]):
                
                if a+b == 2020:
                    return a, b, i, (j+i+1)

    a, b, i, j = iterate()

    print(f"i, j, a, b, a*b: {i}, {j}, {a}, {b}, {a*b}")

def _part_two(vals):
    def iterate():
        for i, a in enumerate(vals):
            for j, b in enumerate(vals[i+1:]):
                for k, c in enumerate(vals[i+j+2:]):
                
                    if a+b+c == 2020:
                        return a, b, c, i, (j+i+1), (k+j+i+2)

    a, b, c, i, j, k = iterate()

    print(f"i, j, k, a, b, c, a*b*c: {i}, {j}, {a}, {b}, {c}, {a*b*c}")


def run(fname: str, part: int):
    with open(fname, 'r') as f:
        lines = f.readlines()

    vals = [int(i.strip()) for i in lines
            if i.strip().isnumeric()]
    print(vals)
    print(f"vals: {len(vals)} lines: {len(lines)}")

    if part == 1:
        _part_one(vals)
    elif part == 2:
        _part_two(vals)
    else:
        print(f"Missing part: {part}")


if __name__ == '__main__':
    fire.Fire(run)
