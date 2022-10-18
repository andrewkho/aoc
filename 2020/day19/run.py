import fire
from typing import *
import re
import itertools
from collections import deque

from dataclasses import dataclass, field
import numpy as np


def _part_one(data):
    raw_rules = data[0]
    msgs = data[1]

    rules = {}
    def get_rule(r: str):
        if r not in rules:
            # raw_rule = ['"a"'] or ['1', '2', '|', '4', '5']
            raw_rule = raw_rules[r]  
            fill = []
            for sr in raw_rule:
                m = re.match(r'^"(.*)"$', sr)
                if m is not None:
                    fill.append(m.groups()[0])
                elif sr.isnumeric():
                    fill.append(f"({get_rule(sr)})")
                else:
                    fill.append(sr)

            rules[r] = ''.join(fill)

        return rules[r]

    rule0 = re.compile('^' + get_rule('0') + '$')

    return sum(rule0.match(msg) is not None for msg in msgs)


def _parse_lines(lines):
    rules = {}
    for i, line in enumerate(lines):
        if line.strip() == '':
            break
        k, v = line.split(':')
        k = k.strip()
        v = v.strip().split(' ')

        assert k not in rules
        rules[k] = v

    msgs = [_.strip() for _ in lines[i+1:]]

    return rules, msgs


def run(fname: str, part: int):
    with open(fname, 'r') as f:
        lines = f.readlines()

    data = _parse_lines(lines)

    print(data)

    if part == 1:
        r = _part_one(data)
        print('part 1: ' + str(r))
    elif part == 2:
        data[0]['8'] = "( 42 )+".split(' ')
        data[0]['11'] = "42 31 | 42 42 31 31 | 42 42 42 31 31 31 | 42 42 42 42 31 31 31 31".split(' ')

        r = _part_one(data)
        print('part 2: ' + str(r))
    else:
        print(f"Missing part: {part}")


if __name__ == '__main__':
    fire.Fire(run)

