import fire
from typing import *
import re
import itertools
from collections import deque

from dataclasses import dataclass, field
import numpy as np


@dataclass
class ASTOp:
    op: str
    l: Union['ASTOp', 'ASTLeaf']
    r: Union['ASTOp', 'ASTLeaf']

    def eval(self):
        if self.op == '+':
            return self.l.eval() + self.r.eval()
        elif self.op == '*':
            return self.l.eval() * self.r.eval()

@dataclass
class ASTLeaf:
    val: int

    def eval(self):
        return self.val


@dataclass
class Parser:
    tokens: List[str]
    t: int = 0

    def operator(self):
        if self.t >= len(self.tokens):
            raise ValueError()
        token = self.tokens[self.t]
        if token not in ('+', '*'):
            raise ValueError(token)
        else:
            self.t += 1
            return token

    def factor(self):
        token = self.tokens[self.t]
        if token.isnumeric():
            self.t += 1
            return ASTLeaf(int(token))
        elif token == '(':
            self.t += 1
            exp = self.expr()
            # Gobble the closing bracket
            token = self.tokens[self.t]
            if token != ')':
                raise ValueError(token)
            self.t += 1
            return exp
        else:
            raise ValueError(token)

    def expr(self):
        l = self.factor()
        while True:
            try:
                op = self.operator()
            except ValueError:
                return l
            
            r = self.factor()
            l = ASTOp(op, l, r)


@dataclass
class Parser2:
    tokens: List[str]
    t: int = 0

    def factor(self):
        token = self.tokens[self.t]
        if token.isnumeric():
            self.t += 1
            return ASTLeaf(int(token))
        elif token == '(':
            self.t += 1
            exp = self.expr()
            # Gobble the closing bracket
            token = self.tokens[self.t]
            if token != ')':
                raise ValueError(token)
            self.t += 1
            return exp
        else:
            raise ValueError(token)

    def expr(self):
        l = self.term()
        while True:
            if self.t >= len(self.tokens):
                return l

            token = self.tokens[self.t]
            if token != '*':
                return l

            op = token
            self.t += 1
            r = self.term()
            l = ASTOp(op, l, r)

    def term(self):
        l = self.factor()
        while True:
            if self.t >= len(self.tokens):
                return l

            token = self.tokens[self.t]
            if token != '+':
                return l

            op = token
            self.t += 1
            r = self.factor()
            l = ASTOp(op, l, r)


TOKENIZER = re.compile(r"[0-9]+|\+|\*|\(|\)")
def _part_one(lines):
    total = 0
    for line in lines:
        tokens = TOKENIZER.findall(line)
        ast = Parser(tokens).expr()
        print(line)
        print(ast.eval())
        total += ast.eval()


    return total


def _part_two(lines):
    total = 0
    for line in lines:
        tokens = TOKENIZER.findall(line)
        ast = Parser2(tokens).expr()
        print(line)
        print(ast.eval())
        total += ast.eval()

    return total


def run(fname: str, part: int):
    with open(fname, 'r') as f:
        lines = f.readlines()

    print(lines)

    if part == 1:
        r = _part_one(lines)
        print('part 1: ' + str(r))
    elif part == 2:
        r = _part_two(lines)
        print('part 2: ' + str(r))
    else:
        print(f"Missing part: {part}")


if __name__ == '__main__':
    fire.Fire(run)

