import fire
from typing import *
from dataclasses import dataclass


def _part_one(data):
    matches = [(policy, pw)
                  for policy, pw in data
                  if policy.is_valid(pw)]
    print("matches: " + str(matches))
    print(f"{len(matches)}")

def _part_two(data):
    matches = [(policy, pw)
                  for policy, pw in data
                  if policy.is_valid2(pw)]
    print("matches: " + str(matches))
    print(f"{len(matches)}")


@dataclass
class Policy:
    min: int
    max: int
    char: str

    @classmethod
    def new(cls, policy: str):
        l, r = policy.split('-')
        min = int(l)

        l2, r2 = r.split(' ')
        max = int(l2)

        char = r2
        return Policy(min, max, char)

    def is_valid(self, pw: str) -> bool:
        count = 0
        for i, c in enumerate(pw):
            if c == self.char:
                count += 1

        return count >= self.min and count <= self.max

    def is_valid2(self, pw: str) -> bool:
        l = pw[self.min-1]
        r = pw[self.max-1]

        return (l == self.char) ^ (r == self.char)


def run(fname: str, part: int):
    with open(fname, 'r') as f:
        lines = f.readlines()

    def process_line(line) -> Tuple[Policy, str]:
        policy, pw = line.split(': ')
        return Policy.new(policy), pw.strip()
        
    data = [process_line(line) for line in lines]

    print(data)
    print(f"data: {len(data)} lines: {len(lines)}")

    if part == 1:
        _part_one(data)
    elif part == 2:
        _part_two(data)
    else:
        print(f"Missing part: {part}")


if __name__ == '__main__':
    fire.Fire(run)
