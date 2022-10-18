import fire
from typing import *
from dataclasses import dataclass


class SeatCode:
    rowsize: int = 7
    row_signs: List[str] = ['F', 'B']
    col_signs: List[str] = ['L', 'R']

    id_row_offset: int = 8

    def __init__(self, code: str):
        self.code = code

    def _to_int(self, code: str, signs: List[str]):
        return int(
            code
            .replace(signs[0], '0')
            .replace(signs[1], '1'), 2)

    def get_row(self) -> int:
        row_code = self.code[:self.rowsize]

        return self._to_int(row_code, self.row_signs)

    def get_col(self) -> int:
        col_code = self.code[self.rowsize:]
        return self._to_int(col_code, self.col_signs)

    def get_id(self) -> int:
        return self.get_row() * self.id_row_offset + self.get_col()


def _part_two(data):
    ids = sorted(c.get_id() for c in data)

    print('\n'.join(str(id) for id in ids))

    prev_id = ids[0]
    for id in ids[1:]:
        if id > prev_id+1:
            break
        prev_id = id

    print(f"id: {id}, prev_id: {prev_id}")

    return prev_id + 1
        

def run(fname: str, part: int):
    with open(fname, 'r') as f:
        lines = f.readlines()

    print(lines)
    print(len(lines))

    data = [SeatCode(line) for line in lines]

    print(data)
    print(f"data: {len(data)} lines: {len(lines)}")

    if part == 1:
        print('max id ' + str(max(c.get_id() for c in data)))
    elif part == 2:
        print('your seat id ' + str(_part_two(data)))
    else:
        print(f"Missing part: {part}")


if __name__ == '__main__':
    fire.Fire(run)
