from bisect import bisect
import inspect
import sys

from constants import DIRECTIONS
from utils import read_input, get_inbounds, day_4b_remove_rolls


def day_1(part='A') -> int:
    data = read_input(day=1)
    position, count, sign = 50, 0, {'R': 1, 'L': -1}
    for direction, *magnitude in data:
        mag = int(''.join(magnitude))
        new_pos = position + sign[direction] * (mag % 100)
        count += not new_pos % 100 if part.upper() == 'A' \
            else (position and not 0 < new_pos < 100) + mag // 100
        position = new_pos % 100
    return count


def day_2(part='A') -> int:
    data = read_input(day=2, delim=',', parse=lambda x: map(int, x.split('-')))
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


def day_3(part='A') -> int:
    abs_max = '9'

    def get_next_max(j, rem: int, bat: str) -> int:
        max_, index = '', None
        for k, bank in enumerate(bat[j:-rem if rem else len(bat)]):
            if bank > max_:
                max_, index = bank, k
                if max_ == abs_max:
                    break
        return index + j

    data, sum_ = read_input(day=3), 0
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


def day_4(part='A') -> int:
    warehouse = read_input(day=4, parse=lambda ln: [c == '@' for c in ln])

    counts = [[0 if b else float('inf') for b in row] for row in warehouse]
    inbounds = get_inbounds(warehouse)
    for y, row in enumerate(warehouse):
        for x, v in enumerate(row):
            counts[y][x] += sum(inbounds(y + yi, x + xi) and
                                warehouse[y + yi][x + xi]
                                for yi, xi in DIRECTIONS)

    if part.upper() == 'A':
        return sum(v < 4 for row in counts for v in row)
    return day_4b_remove_rolls(counts)


def day_5(part='A') -> int:
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

    fresh, ingredients = read_input(day=5, delim='', parse=parse).pop()

    if not part.upper() == 'A':
        return sum(stop + 1 - start for start, stop in fresh)

    n, sum_ = len(fresh), 0
    for food in ingredients:
        index = bisect(fresh, (food,))
        if index == -1:
            continue
        sum_ += not index == -1 and \
            fresh[index-1][0] <= food <= fresh[index-1][1]
    return sum_


if __name__ == '__main__':
    args = sys.argv[1:] if sys.argv[1:] else range(1, 12)
    args = (f'day_{i}' for i in args)
    members = inspect.getmembers(inspect.getmodule(inspect.currentframe()))
    funcs = {name: member for name, member in members
             if inspect.isfunction(member)}
    for day in args:
        if day not in funcs:
            print(f'{day}()= NotImplemented')
            continue
        print(f'{day}()= {funcs[day]()}')
        print(f'{day}(part="B")= {funcs[day](part="B")}')
