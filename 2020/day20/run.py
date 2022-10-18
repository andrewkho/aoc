import math
import fire
from typing import *
import re
import itertools
from collections import deque

from dataclasses import dataclass, field
import numpy as np



def get_orientation(t, ot, et, u):
    """
    for a fixed orientation of t ot, find the edge pairs
        of t and u that match, along with corresponding 
        orientation of u
    """
    matches = []
    e = t.edge(et, ot)
    eu = (et + 2) % 4
    for ou in range(8):
        if e == u.edge(eu, ou):
            matches.append(ou)
        
    return matches


def get_matching_edges(t, ot, u):
    """
    for a fixed orientation of t ot, find the edge pairs
        of t and u that match, along with corresponding 
        orientation of u
    """
    matches = []
    for et in range(4):
        e = t.edge(et, ot)

        for eu, ou in itertools.product(range(4), range(8)):
            if e == u.edge(eu, ou):
                matches.append((et, eu, ou))
        
    return matches
    

def get_matches(t, data):
    matches = {}
    for et in range(4):
        for j, u in data.items():
            if t is u:
                continue
            matching_edges = get_matching_edges(t, 0, u)
            if len(matching_edges) > 0:
                matches[j] = matching_edges

    return matches


def _part_one(data):
    corners = []

    matches = {}
    for i, t in data.items():
        m = get_matches(t, data)
        matches[i] = m
        if len(m) == 2:
            corners.append((i, t))

    print(corners)
    print(f"len corners: {len(corners)}")
    counts = {k: len(v) for k, v in matches.items()}
    print(f"all matches: {matches}")
    
    prod = 1
    for c in corners:
        prod *= c[0]

    return prod


def _part_two(data):
    corners = []

    matches = {}
    for i, t in data.items():
        m = get_matches(t, data)
        matches[i] = m
        if len(m) == 2:
            corners.append((i, t))

    print(corners)

    i0 = corners[0][0]
    t0 = corners[0][1]

    s = set()
    for j, matching_edges in matches[i0].items():
        for x in matching_edges:
            s.add(x[0])

    assert len(s) == 2
    print(s)
    if s == {0, 1}:
        o0 = 1
    elif s == {1, 2}:
        o0 = 2
    elif s == {2, 3}:
        o0 = 3
    elif s == {3, 0}:
        o0 = 0
    else:
        ValueError("Invalid starting corner: {c}")

    board = dict()
    board[0, 0] = PuzzlePiece(i0, t0, o0, matches[i0])

    consumed = set()
    consumed.add(i0)
    
    N = int(math.sqrt(len(data)))
    print(f"board length: {N}")
    # Now with a seeded board can begin finding pieces to insert
    for j in range(N):
        for i in range(N):
            if (j, i) in board:
                continue

            # Find correct orientation
            if i == 0:
                piece = board[j-1, i]
                look_for_edge = Tile.DOWN
            else:
                piece = board[j, i-1]
                look_for_edge = Tile.RIGHT

            for u in piece.matches:
                if u in consumed:
                   continue

                ou = get_orientation(piece.tile, 
                                     piece.orientation,
                                     look_for_edge,
                                     data[u])
                if len(ou) == 0:
                    continue
                if len(ou) > 1:
                    raise ValueError(i, j, u, ou)

                break 

            if len(ou) == 0:
                 raise ValueError(i, j, board)

            board[j, i] = PuzzlePiece(u, data[u], ou[0], matches[u])

    flat_board = make_board(board, N, with_border=True)
    print('\n'.join(flat_board))

    return search_board(board, N)


MONSTER = ['                  # ', 
           '#    ##    ##    ###', 
           ' #  #  #  #  #  #   ']

def search_board(board, N):
    flat_board = make_board(board, N, with_border=False)
    # LEt's try flipping entire board
    rotated_board = []
    for r in flat_board:
        rotated_board.append(r[::-1])

    flat_board = rotated_board


    def check_match(i, j):
        if i+len(MONSTER[0]) > len(flat_board[0]):
            return False
        if j+len(MONSTER) > len(flat_board):
            return False
        
        for mj, mrow in enumerate(MONSTER):
            for mi, m in enumerate(mrow):
                if m == ' ':
                    continue
                if flat_board[j+mj][i+mi] != '#':
                    return False

        return True

    def zero_out(i, j):
        for mj, mrow in enumerate(MONSTER):
            new_row = []
            for mi, m in enumerate(mrow):
                if m == ' ':
                    new_row.append(flat_board[j+mj][i+mi])
                else:
                    new_row.append('.')
            new_row = flat_board[j+mj][:i] + ''.join(new_row) + flat_board[j+mj][i+mi+1:]
            flat_board[j+mj] = new_row

    matches = []
    for j in range(len(flat_board)):
        for i in range(len(flat_board[0])):
            if check_match(i, j):
                matches.append((i, j))
    
    print(matches)
    if len(matches) == 0:
        raise ValueError()

    for match in matches:
        zero_out(*match)

    print('\n'.join(flat_board))

    count = 0
    for r in flat_board:
        for c in r:
            if c == '#':
                count += 1


    return count


def make_board(board, N, with_border = True):
    th = len(board[0, 0].tile._tile)

    image = []
    for j in range(N):
        delta = 0
        if not with_border:
            delta = 1
        for tj in range(delta, th-delta):
            row = []
            for i in range(N):
                piece = board[j, i]
                line = piece.tile.get_row(tj, piece.orientation)
                if with_border:
                    row.append(line)
                else:
                    row.append(line[delta:-delta])
            if with_border:
                image.append(' '.join(row))
            else:
                image.append(''.join(row))

        if with_border:
            image.append('\n')

    return image

@dataclass
class PuzzlePiece:
    n: int
    tile: 'Tile'
    orientation: int
    matches: dict


class Tile:
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def __init__(self, tile: List[str]):
        self._tile = tile
        self._edges = [  # up right down left
            ''.join(tile[0]),
            ''.join([c[-1] for c in tile]),
            ''.join(tile[-1]),
            ''.join([c[0] for c in tile]),
        ]

    def __str__(self):
        return '\n' + '\n'.join(self._tile) + '\n'

    def __repr__(self):
        return self.__str__()
        

    def edge(self, edge, orientation):
        e = (edge - orientation) % 4
        if (4 <= orientation < 8) and edge % 2 == 1:
            e = (e + 2) % 4

        if e in (0, 2) and orientation in (2, 3, 4, 7):
            return self._edges[e][::-1]
        elif e in (1, 3) and orientation in (1, 2, 6, 7):
            return self._edges[e][::-1]
        else:
            return self._edges[e]

    def get_row(self, row, orientation):
        if orientation in (0, 4):
            ret = self._tile[row]
        elif orientation in (2, 6):
            ret = self._tile[len(self._tile) - row - 1]
        elif orientation in (1, 5):
            ret = ''.join([r[row] for r in self._tile])
        elif orientation in (3, 7):
            ret = ''.join([r[len(self._tile) - row - 1] for r in self._tile])

        if orientation in (0, 3, 5, 6):
            flip = False
        elif orientation in (1, 2, 4, 7):
            flip = True

        if flip:
            return ret[::-1]
        else:
            return ret




def _parse_lines(lines):
    data = {}
    buf = []
    n = None
    for line in lines:
        if line.startswith('Tile'):
            # All tiles are 4 digits and start 
            # after "Tile "
            n = int(line[5:9])
        elif line.strip() == '':
            data[n] = Tile(buf)
            buf = []
            n = None
        else:
            buf.append(line.strip())

    if n is not None:
        raise ValueError(n)

    return data


def run(fname: str, part: int):
    with open(fname, 'r') as f:
        lines = f.readlines()

    data = _parse_lines(lines)

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

