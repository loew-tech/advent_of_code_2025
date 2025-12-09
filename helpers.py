import heapq
from typing import List, Tuple, Callable, Set

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


def day_9b_largest_inner_rectangle(
        data,
        areas
) -> int:
    def get_perimeter():
        p = set()
        for i_ in range(len(data)):
            x1, y1 = data[i_-1]
            x2, y2 = data[i_]
            if x1 == x2:
                for y_ in range(min(y1, y2), max(y1, y2) + 1):
                    p.add((x1, y_))
            elif y1 == y2:
                for x_ in range(min(x1, x2), max(x1, x2) + 1):
                    p.add((x_, y1))
        return p

    max_, perimeter = None, get_perimeter()
    while areas and (entry := heapq.heappop(areas)):
        ar, (i, j) = entry
        ar = -ar
        x_min, x_max = min(data[i][0], data[j][0]), max(data[i][0], data[j][0])
        y_min, y_max = min(data[i][1], data[j][1]), max(data[i][1], data[j][1])
        bad = False
        for x, y in perimeter:
            if bad := x_min < x < x_max and y_min < y < y_max:
                break
        if bad:
            continue
        return ar
    return -1
