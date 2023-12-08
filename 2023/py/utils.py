from dataclasses import dataclass
from typing import List


def get_input(f: str) -> str:
    return "../inputs/" + f.rsplit("/", 1)[1].replace(".py", ".txt")


@dataclass
class Grid:
    X: int
    Y: int
    X0: int = 0
    Y0: int = 0
    
    def neighbours(self, x, y):
        for dx, dy in itertools.product([-1, 0, 1], [-1, 0, 1]):
            if not self.X0 <= x+dx < self.X:
                continue
            if not self.Y0 <= y+dy < self.Y:
                continue
            yield x+dx, y+dy


def get_primes(up_to: int) -> List[int]:
    sieve = [True] * (up_to // 2)
    sieve[0:2] = [False, False]
    for c in range(2, len(sieve)//2):
        for i in range(2*c, len(sieve), c):
            sieve[i] = False
    return [i for i, prime in enumerate(sieve) if prime]


