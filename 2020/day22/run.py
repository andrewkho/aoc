import math
import fire
from typing import *
import re
import itertools
from collections import deque

from dataclasses import dataclass, field
import numpy as np


def _part_one(data):
    decks = data
    round = 0
    while True:
        if len(decks[0]) == 0 or len(decks[1]) == 0:
            break
        print(f"round {round}")
        c0 = decks[0].popleft()
        c1 = decks[1].popleft()
        print(f"c0: {c0} c1: {c1}")
        if c0 > c1:
            print("p0 won!")
            decks[0].append(c0)
            decks[0].append(c1)
        elif c1 > c0:
            print("p1 won!")
            decks[1].append(c1)
            decks[1].append(c0)
        else:
            raise ValueError()
        round += 1

    winner = decks[0] if len(decks[0]) > 0 else decks[1]

    return sum(
        (len(winner) - i) * c 
        for i, c in enumerate(winner)
    )


@dataclass
class Result:
    winner: int
    deck0: Any
    deck1: Any


def _recursive_combat(deck0, deck1, game):
    r = 0
    total_sets = set()
    while True:
        if len(deck0) == 0 or len(deck1) == 0:
            winner = 0 if len(deck1) == 0 else 1
            return Result(winner, deck0, deck1)
        if (tuple(deck0), tuple(deck1)) in total_sets:
            return Result(0, deck0, deck1)
        else:
            total_sets.add((tuple(deck0), tuple(deck1)))

        print(f"round {r}, game {game}")
        c0 = deck0.popleft()
        c1 = deck1.popleft()
        if c0 <= len(deck0) and c1 <= len(deck1):
            subdeck0 = deque([deck0[_] for _ in range(c0)])
            subdeck1 = deque([deck1[_] for _ in range(c1)])
            result = _recursive_combat(subdeck0, subdeck1, game+1)
            winner = result.winner
        else:
            winner = 0 if c0 > c1 else 1

        print(f"c0: {c0} c1: {c1}")
        if winner == 0:
            print("p0 won!")
            deck0.append(c0)
            deck0.append(c1)
        elif winner == 1:
            print("p1 won!")
            deck1.append(c1)
            deck1.append(c0)
        else:
            raise ValueError()

        r += 1
    

def _part_two(data):
    decks = data

    result = _recursive_combat(decks[0], decks[1], 0)

    winning_deck = result.deck0 if result.winner == 0 else result.deck1

    return sum(
        (len(winning_deck) - i) * c 
        for i, c in enumerate(winning_deck)
    )


def run(fname: str, part: int):
    with open(fname, 'r') as f:
        lines = f.readlines()

    data = [deque(), deque()]
    player = 0
    for line in lines:
        if line.startswith('Player'):
            continue
        if line.strip() == '':
            player += 1
            continue

        data[player].append(int(line.strip()))

    print(str(data))

    if part == 1:
        r = _part_one(data)
        print('part 1: ' + str(r))
    elif part == 2:
        r = _part_two(data)
        print('part 2: ' + str(r))
    else:
        print(f"Missing part: {part}")


if __name__ == '__main__':
    fire.Fire(run)

