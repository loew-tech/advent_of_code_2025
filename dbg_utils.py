from typing import Iterable, Tuple, Callable, List

from bs4 import BeautifulSoup
import requests


from constants import ADVENT_URI
from utils import _process_input


def get_test_input(
        day: int | str,
        year: int | str = 2025,
        delim: str = '\n',
        parse: Callable[[str], any] = None
) -> Tuple[List[any] | str, str]:
    problem = requests.get(f'{ADVENT_URI}{year}/day/{day}')
    soup = BeautifulSoup(problem.content, 'html.parser')
    # @TODO: handle retrieving test input for part b
    input_ = soup.find('pre').code
    answer = soup.find_all('code')[:-1]
    return _process_input(input_.get_text(), delim, parse), answer.get_text()


def print_grid(grid: Iterable[Iterable], spacer='') -> None:
    for row in grid:
        print(spacer.join(str(i) for i in row))
