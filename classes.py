import copy
from typing import List, Set, Tuple


class Machine:

    @classmethod
    def from_line(cls, line: str):
        lghts = {i for i, v in enumerate(line[1:line.index(']') + 1]) if
                 v == '#'}
        *btns, volts = line.split()[1:]
        btns = [{int(i) for i in part[1:-1].split(',')} for part in btns]
        volts = tuple(int(i) for i in volts[1:-1].split(','))
        return cls(lghts, btns, volts)

    def __init__(self, lights: Set[int],
                 btns: List[Set[int]],
                 voltages: Tuple[int]):
        self.lights, self.btns, self.voltages = lights, btns, voltages

    def turn_on(self) -> int:
        candidate, cnt = [set() for _ in self.btns], 0
        while cnt := cnt + 1:
            new_ = []
            for candidate in candidate:
                for btn in self.btns:
                    new_candidate = candidate ^ btn
                    if new_candidate == self.lights:
                        return cnt
                    new_.append(new_candidate)
            candidate = new_
        return cnt

    def __repr__(self):
        return f'Machine({self.lights}, {self.btns}, {self.voltages})'


class Node:

    def __init__(self, id_: str, neighbors: List[str]):
        self.id_, self.neighbors, self._i = id_, neighbors, 0

    def get_next_neighbor(self) -> str | None:
        self._i += 1
        return self.neighbors[self._i-1] if self._i-1 < len(self.neighbors) \
            else None

    def get_current_neighbor(self) -> str:
        return self.neighbors[self._i] if self._i < len(self.neighbors) \
            else None

    def copy(self):
        return copy.copy(self)

    def __repr__(self):
        return f'Node({self.id_}, {self.neighbors}, {self._i})'
