import heapq
from typing import List, Tuple, Callable, Set, Dict

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


def day_11_dfs(graph: Dict[str, List[str]], start, stop: str) -> int:
    to_search, visited, cnt = graph.get(start, []), set(), 0
    while to_search:
        node = to_search.pop()
        visited.add(node)
        cnt += node == stop
        to_search.extend(graph.get(node, []))
    return cnt

