from typing import Iterable, Tuple, Callable, List

from bs4 import BeautifulSoup
import requests


from constants import ADVENT_URI


def get_test_input(
        day: int | str,
        year: int | str = 2025,
) -> str:
    problem = requests.get(f'{ADVENT_URI}{year}/day/{day}')
    soup = BeautifulSoup(problem.content, 'html.parser')
    # @TODO: handle retrieving test input for part b
    input_ = soup.find('pre').code
    # @TODO: handle validating against this
    # answer = soup.find_all('code')[:-1]
    return input_.get_text()


def print_grid(grid: Iterable[Iterable], spacer='') -> None:
    for row in grid:
        print(spacer.join(str(i) for i in row))
