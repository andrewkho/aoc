import fire
from typing import *
from dataclasses import dataclass

import rules

ALLOWED = {
    "byr",  # (Birth Year)
    "iyr",  # (Issue Year)
    "eyr",  # (Expiration Year)
    "hgt",  # (Height)
    "hcl",  # (Hair Color)
    "ecl",  # (Eye Color)
    "pid",  # (Passport ID)
    "cid",  # (Country ID)
}


VALIDATION = {
    "byr",  # (Birth Year)
    "iyr",  # (Issue Year)
    "eyr",  # (Expiration Year)
    "hgt",  # (Height)
    "hcl",  # (Hair Color)
    "ecl",  # (Eye Color)
    "pid",  # (Passport ID)
}

@dataclass
class Passport:
    keys: List[str]
    values: List[str]

    def is_valid(self):
        keyset = set(self.keys)
        if len(keyset) != len(self.keys):
            return False

        if keyset == ALLOWED or keyset == VALIDATION:
            return True

        return False

    def is_valid2(self):
        if not self.is_valid():
            return False

        for key, val in zip(self.keys, self.values):
            rule = rules.RULES[key]
            if not rule(val):
                return False

        return True

def _part_one(data):
    valids = [p for p in data if p.is_valid()]

    print(valids)

    return len(valids)


def _part_two(data):
    valids = [p for p in data if p.is_valid2()]

    print(valids)

    return len(valids)

def run(fname: str, part: int):
    with open(fname, 'r') as f:
        lines = f.readlines()

    raw_passports = []
    s = ''
    for line in lines:
        line = line.strip()
        if line == '':
            raw_passports.append(s[1:])  # first char is always a space
            s = ''
            continue

        s += ' ' + line
    raw_passports.append(s[1: ])
        
    print(raw_passports)
    print(len(raw_passports))

    def process_line(line):
        keys = []
        vals = []
        for token in line.split(' '):
            k, v = token.split(':')
            keys.append(k)
            vals.append(v)

        return Passport(keys, vals)
        
    data = [process_line(line) for line in raw_passports]

    print(data)
    print(f"data: {len(data)} lines: {len(lines)}")

    if part == 1:
        print('num_valid ' + str(_part_one(data)))
    elif part == 2:
        print('num_valid 2: ' + str(_part_two(data)))
    else:
        print(f"Missing part: {part}")


if __name__ == '__main__':
    fire.Fire(run)
