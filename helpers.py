# @TODO: move to helpers
from typing import List

from constants import DIRECTIONS
from utils import inbounds


def day_4b_remove_rolls(counts: List[List[int]]):
    to_move = set((y, x) for y, row in enumerate(counts)
                  for x, v in enumerate(row) if v < 4)
    removed = 0
    while to_move:
        next_search = set()
        for y, x in sorted(to_move):
            removed += 1
            for yi, xi in DIRECTIONS:
                if not inbounds(y + yi, x + xi, counts) or \
                        (y + yi, x + xi) in to_move:
                    continue
                counts[y + yi][x + xi] -= 1
                if counts[y + yi][x + xi] < 4:
                    next_search.add((y + yi, x + xi))
            counts[y][x] = float('inf')
        to_move = next_search
    return removed