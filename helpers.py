import heapq
from collections import defaultdict
from typing import List, Tuple, Callable, Set, Dict

from classes import Node
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
        for i_, (x2, y2) in enumerate(data):
            x1, y1 = data[i_ - 1]
            x1, x2 = (x1, x2) if x1 <= x2 else (x2, x1)
            y1, y2 = (y1, y2) if y1 <= y2 else (y2, y1)
            for x_ in range(x1, x2+1):
                p.add((x_, y1))
            for y_ in range(y1, y2+1):
                p.add((x1, y_))
        return p

    max_, perimeter = None, get_perimeter()
    while areas and (entry := heapq.heappop(areas)):
        ar, (i, j) = entry
        ar = -ar
        x_min, x_max = min(data[i][0], data[j][0]), max(data[i][0], data[j][0])
        y_min, y_max = min(data[i][1], data[j][1]), max(data[i][1], data[j][1])
        if any(x_min < x < x_max and y_min < y < y_max for x, y in perimeter):
            continue
        return ar
    return -1


def day_11_dfs(graph: Dict[str, Node], start, stop: str) -> int:
    def append_non_none(v: str | None) -> None:
        if v in graph:
            to_search.append(graph[v])

    paths_to_stop, to_search, cnt = defaultdict(int), [graph[start]], 0
    while to_search:
        while to_search and to_search[-1].get_current_neighbor() is None:
            to_search.pop()
        if not to_search:
            return paths_to_stop[start]
        nghbor = to_search[-1].get_next_neighbor()
        if nghbor == stop or nghbor in paths_to_stop:
            new_paths = 1 if nghbor == stop else paths_to_stop[nghbor]
            for n in to_search:
                paths_to_stop[n.id_] += new_paths
        append_non_none(nghbor)
    return paths_to_stop[start]
