import multiprocessing as mp
from typing import *
from timer import Timer
import utils
from utils import get_input, Grid
from collections import defaultdict, Counter, deque
from dataclasses import dataclass, field
import itertools
import bisect
import functools
import copy
import heapq

import re

@dataclass
class Brick:
    p0: List[int]
    p1: List[int]
    id_: int

    def __post_init__(self):
        self.bb = (
            (min(self.p0[0], self.p1[0]), (max(self.p0[0], self.p1[0]))),
            (min(self.p0[1], self.p1[1]), (max(self.p0[1], self.p1[1]))),
        )
        self.z = min(self.p0[2], self.p1[2])
        self.ht = max(self.p0[2], self.p1[2]) - self.z 


@dataclass
class Kdtree:
    dim: int
    split: int
    left: "Kdtree" = None
    right: "Kdtree" = None
    leaves: List[Brick] = None

    def intersect(self, brick):
        result = []
        if self.left:
            result += self.left.intersect(brick)
        if self.right:
            result += self.right.intersect(brick)

        for leaf in self.leaves:
            if brick.bb[0][1] < leaf.bb[0][0] or leaf.bb[0][1] < brick.bb[0][0]:
                continue
            elif brick.bb[1][1] < leaf.bb[1][0] or leaf.bb[1][1] < brick.bb[1][0]:
                continue
            result.append(leaf)

        return result

def build_tree(bricks, dim=0, depth=0) -> Kdtree:
    if len(bricks) == 0:
        return None
    if len(bricks) == 1:
        return Kdtree(dim, bricks[0].bb[dim][0], leaves=[bricks[0]])

    bricks = sorted(bricks, key=lambda x: x.bb[dim][0])
    m = len(bricks)//2
    split = bricks[m].bb[dim][0]
    
    lbricks, rbricks, leaves = [], [], []
    for b in bricks:
        if b.bb[dim][1] < split:
            lbricks.append(b)
        elif b.bb[dim][0] > split:
            rbricks.append(b)
        else:
            leaves.append(b)
    left = build_tree(lbricks, 1-dim, depth+1)
    right = build_tree(rbricks, 1-dim, depth+1)
    return Kdtree(dim, split, left, right, leaves)


def main():
    infile = get_input(__file__)
    with Timer(f"Reading from {infile}..."):
        with open(infile, "r") as f:
            lines = []
            for line in f.readlines():
                lines.append(line.strip())

    with Timer("part 1"):
        bricks = []
        for i, line in enumerate(lines):
            l, r = line.split("~")
            bricks.append(
                Brick(
                    [int(x) for x in l.split(",")], 
                    [int(x) for x in r.split(",")],
                    id_=i,
                )
            )

        tree = build_tree(bricks)

        bricks = sorted(bricks, key=lambda x: x.z)
        stopped = [False]*len(bricks)
        def step(remove = None, max_steps = float("inf")):
            moves = 0
            move_ids = []
            for brick in bricks:
                if brick.id_ == remove or (remove is None and stopped[brick.id_]):
                    continue
                can_move = True
                if brick.z == 1:
                    can_move = False
                    stopped[brick.id_] = True
                else:
                    candidates = tree.intersect(brick)
                    candidates = sorted(candidates, key=lambda x: -x.z)
                    for o in candidates:
                        if o == brick or o.id_ == remove:
                            continue
                        if brick.z == o.z + o.ht + 1:
                            can_move = False
                            if remove is None and stopped[o.id_]:
                                stopped[brick.id_] = True
                            break
                if can_move:
                    moves += 1
                    move_ids.append(brick.id_)
                    if remove is None or max_steps > 1:
                        brick.z -= 1
                    elif max_steps == 1:
                        break

            return moves, move_ids

        while True:
            moves, _ = step()
            if moves == 0:
                break

        print("settled")
        result = 0
        for i, brick in enumerate(bricks):
            if i % 100 == 0:
                print("part 1 brick", i, brick.id_)
            moves, _ = step(brick.id_, max_steps=1)

            if moves == 0:
                result += 1

        print("part1:", result)

    with Timer("part 2"):
        result = 0
        orig_z = [brick.z for brick in bricks]
        for i, brick in enumerate(bricks):
            for b, z in zip(bricks, orig_z):
                b.z = z

            stopped = [False]*len(bricks)
            _, move_ids = step(brick.id_)
            move_set = set(move_ids)
            while len(move_ids) > 0:
                _, move_ids = step(brick.id_)
                move_set.update(move_ids)
            result += len(move_set)
            if i % 100 == 0:
                print("part 2 brick", i, brick.id_, len(move_set))
        print("part 2:", result)


if __name__ == '__main__':
    main()
