import inspect
import sys

from utils import read_input


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
    def parse(dat):
        ret = []
        for entry in dat:
            ret.append(map(int, entry.split('-')))
        return ret

    data = read_input(day=2, delim=',', parse=parse)
    sum_ = 0
    for low, high in data:
        for i in range(low, high+1):
            s = str(i)
            mid = len(s) // 2
            if s[:mid] == s[mid:]:
                sum_ += i
            elif not part.upper() == 'A':
                for j in range(1, len(s)//2 + 1):
                    if set(s.split(s[:j])) == {''}:
                        sum_ += i
                        break
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
