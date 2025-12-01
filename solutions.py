import inspect
import sys


from utils import test_problem


def day_1(part='A') -> int:
    test_problem(day=1)


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
