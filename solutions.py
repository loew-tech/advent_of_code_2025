import inspect
import sys

from utils import read_input


def day_1(part='A') -> int:
    data = read_input(day=1)
    position, count, sign = 50, 0, {'R': 1, 'L': -1}
    for direction, *magnitude in data:
        position = (position + sign[direction] * int(''.join(magnitude))) % 100
        count += not position
    return count


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
