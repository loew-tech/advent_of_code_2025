import heapq
from bisect import bisect
from collections import defaultdict
from functools import reduce
import inspect
import sys

from constants import OPS_DICT
from dbg_utils import get_expected
from helpers import *
from utils import read_input, get_inbounds


def day_1(part='A', test=False) -> int:
    data = read_input(day=1, testing=test)
    position, count, sign = 50, 0, {'R': 1, 'L': -1}
    for direction, *magnitude in data:
        mag = int(''.join(magnitude))
        new_pos = position + sign[direction] * (mag % 100)
        count += not new_pos % 100 if part.upper() == 'A' \
            else (position and not 0 < new_pos < 100) + mag // 100
        position = new_pos % 100
    return count


def day_2(part='A', test=False) -> int:
    data = read_input(day=2,
                      delim=',',
                      parse=lambda x: map(int, x.split('-')),
                      testing=test)
    sum_ = 0
    for low, high in data:
        for i in range(low, high + 1):
            s = str(i)
            mid = len(s) // 2
            if s[:mid] == s[mid:]:
                sum_ += i
            elif not part.upper() == 'A':
                for j in range(1, len(s) // 2 + 1):
                    if set(s.split(s[:j])) == {''}:
                        sum_ += i
                        break
    return sum_


def day_3(part='A', test=False) -> int:
    abs_max = '9'

    def get_next_max(j, rem: int, bat: str) -> int:
        max_, index = '', None
        for k, bank in enumerate(bat[j:-rem if rem else len(bat)]):
            if bank > max_:
                max_, index = bank, k
                if max_ == abs_max:
                    break
        return index + j

    data, sum_ = read_input(day=3, testing=test), 0
    sum_ = 0

    for battery in data:
        limit = 2 if part.upper() == 'A' else 12
        banks, i, remaining = [], -1, limit
        while len(banks) < limit:
            remaining -= 1
            i = get_next_max(i + 1, remaining, battery)
            banks.append(battery[i])
        sum_ += int(''.join(banks))
    return sum_


def day_4(part='A', test=False) -> int:
    warehouse = read_input(day=4,
                           parse=lambda ln: [c == '@' for c in ln],
                           testing=test)

    counts = [[0 if b else float('inf') for b in row] for row in warehouse]
    inbounds_ = get_inbounds(warehouse)
    for y, row in enumerate(warehouse):
        for x, v in enumerate(row):
            counts[y][x] += sum(inbounds_(y + yi, x + xi) and
                                warehouse[y + yi][x + xi]
                                for yi, xi in DIRECTIONS)

    if part.upper() == 'A':
        return sum(v < 4 for row in counts for v in row)
    return day_4b_remove_rolls(counts)


def day_5(part='A', test=False) -> int:
    def merge(
            intervals: list[tuple[int, ...]]
    ) -> list[tuple[int, int]]:
        merged = [intervals[0]]
        for start, end in intervals[1:]:
            last_start, last_end = merged[-1]
            if start <= last_end:
                merged[-1] = (last_end if last_start > start else last_start,
                              max(last_end, end))
            else:
                merged.append((start, end))
        return merged

    def parse(data: str):
        frsh, ing = data.split('\n\n')
        frsh = [tuple(int(y) for y in x.split('-')) for
                x in frsh.split('\n')]
        ing = map(int, ing.split('\n')[:-1])
        return merge(sorted(frsh, key=lambda x: (x[0], -x[1]))), ing

    fresh, ingredients = read_input(day=5,
                                    delim='',
                                    parse=parse,
                                    testing=test).pop()

    if not part.upper() == 'A':
        return sum(stop + 1 - start for start, stop in fresh)

    n, sum_ = len(fresh), 0
    for food in ingredients:
        index = bisect(fresh, (food,))
        if index == -1:
            continue
        sum_ += fresh[index - 1][0] <= food <= fresh[index - 1][1]
    return sum_


def day_6(part='A', test=False) -> int:
    def parse_a(data: str):
        lines = [[c for c in ln.split(' ') if c.strip()] for
                 ln in data.strip().split('\n')]
        return [list(reversed(x)) for x in zip(*lines)]

    def parse_b(data: str):
        lines = [[*ln] for
                 ln in data.rstrip().split('\n')]
        max_ = max(len(ln) for ln in lines)
        lines = [['']*(max_ - len(ln)) + ln for ln in lines]
        lines = [list(x) for x in zip(*lines)]
        probs, prob, op_ = [], [], None
        for *p, o in lines:
            if o in OPS_DICT:
                op_ = o
            num = ''.join(p).strip()
            if not num:
                probs.append([op_, *prob])
                prob, op_ = [], None
                continue
            prob.append(num)
        probs.append([op_, *prob])
        return probs

    parse = parse_a if part.upper() == 'A' else parse_b
    problems = read_input(day=6, delim='', parse=parse, testing=test,)[0]
    return sum(reduce(OPS_DICT[op], map(int, vals)) for op, *vals in problems)


def day_7(part='A', test=False) -> int:
    grid = read_input(day=7, delim='\n', testing=test)
    inbounds_ = get_inbounds(grid)

    def cond_add(d: defaultdict, y_, x_, cnt_: int) -> None:
        if not inbounds_(y_, x_):
            return
        d[x_] += cnt_

    splits, y = 0, 0
    (to_search := defaultdict(int))[grid[0].index('S')] = 1
    while to_search and (y := y+1):
        next_search = defaultdict(int)
        for x, cnt in to_search.items():
            if grid[y][x] == '^':
                splits += 1 if part.upper() == 'A' else cnt
                cond_add(next_search, y, x-1, cnt)
                cond_add(next_search, y, x+1, cnt)
                continue
            cond_add(next_search, y+1, x, cnt)
        to_search = next_search
    return splits + (not part.upper() == 'A')


def day_8(part='A', test=False) -> int:
    def distance(pt, pt2) -> int:
        return sum((p - pt2[i_])**2 for i_, p in enumerate(pt))

    data = read_input(day=8,
                      parse=lambda x: tuple(map(int, x.split(','))),
                      testing=test)

    edges = set()
    distances = []
    for i, box in enumerate(data):
        for j, b in enumerate(data):
            if (i, j) in edges or i == j:
                continue
            distances.append((distance(box, b), box, b))
            edges.add((i, j))
            edges.add((j, i))
    heapq.heapify(distances)

    box_to_circuit = {}
    for i in range(10 if testing else 1_000):
        _, b1, b2 = heapq.heappop(distances)
        if b1 in box_to_circuit and b2 in box_to_circuit:
            for b in box_to_circuit[b2]:
                box_to_circuit[b1].add(b)
                box_to_circuit[b] = box_to_circuit[b1]
        elif b1 in box_to_circuit:
            box_to_circuit[b1].add(b2)
        elif b2 in box_to_circuit:
            box_to_circuit[b2].add(b1)
            box_to_circuit[b1] = box_to_circuit[b2]
        else:
            box_to_circuit[b1] = {b1, b2}
        box_to_circuit[b2] = box_to_circuit[b1]

    used, h2 = set(), []
    for k, set_ in box_to_circuit.items():
        if k in used:
            continue
        used = {*used, *set_}
        heapq.heappush(h2, -len(set_))

    prod = 1
    for _ in range(3):
        prod *= -heapq.heappop(h2)
    return prod


if __name__ == '__main__':
    def print_result(d: int,
                     expected, part: str,
                     result: int | str) -> None:
        if expected == str(result):
            print(f'PASS {d}{part}: {d}({part}) = {result}.')
            return
        print(f'FAILED {d}{part}: Expected = {expected}. {d}({part}) ='
              f' {result}')

    def test_days(days):
        for day_ in days:
            if day_ not in funcs:
                print(f'{day}()= NotImplemented')
                continue
            expected, result = get_expected(day=day_), funcs[day_](test=True)
            print_result(day_, expected, 'A', result)

            expected = get_expected(day=day_, part='B')
            result = funcs[day_](test=True, part='B')
            print_result(day_, expected, 'B', result)


    testing = '-t' in sys.argv[1:]
    args = (f'day_{i}' for i in (sys.argv[1:] if
            sys.argv[1:] else range(1, 13)) if i.isnumeric())
    members = inspect.getmembers(inspect.getmodule(inspect.currentframe()))
    funcs = {name: member for name, member in members
             if inspect.isfunction(member)}

    if testing:
        test_days(args)

    for day in args:
        if day not in funcs:
            print(f'{day}()= NotImplemented')
            continue
        print(f'{day}() = {funcs[day]()}')
        print(f'{day}(part="B") = {funcs[day](part="B")}')
