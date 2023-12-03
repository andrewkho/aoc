from dataclasses import dataclass


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

