from datetime import datetime
from http import HTTPStatus
import requests
from typing import List, Callable, Iterable

from constants import ADVENT_URI


def read_input(
        day: int | str,
        year: int | str = 2025,
        delim: str = '\n',
        parse: Callable[[str], any] = None
) -> List[any] | str:
    year = year if year is not None else datetime.now().year
    with open('.env') as env_:
        session_id = env_.read().strip().split('\n')[0]
    response = requests.get(f'{ADVENT_URI}{year}/day/{day}/input',
                            cookies={'session': session_id})
    data = None
    if response.status_code == HTTPStatus.OK:
        data = response.text.strip().split(delim) if delim else response.text
    return data if parse is None else [parse(e) for e in data]


def get_inbounds(
        grid: List[List[any] | str]
) -> Callable[[int, int], bool]:
    return lambda y, x: inbounds(y, x, grid)


def inbounds(y, x: int, grid: List[List[any] | str]) -> bool:
    return 0 <= y < len(grid) and 0 <= x < len(grid[y])
