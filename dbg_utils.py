import os
from typing import Iterable

from bs4 import BeautifulSoup
import requests


from constants import ADVENT_URI, TESTS_PATH


def get_test_input(
        day: int | str,
        year: int | str = 2025,
) -> str:
    if os.path.exists(f'{TESTS_PATH}{day}.txt'):
        print(f'retrieving {day} test from file')
        with open(f'{TESTS_PATH}{day}.txt') as in_:
            return in_.read()

    problem = requests.get(f'{ADVENT_URI}{year}/day/{day}')
    soup = BeautifulSoup(problem.content, 'html.parser')
    input_ = soup.find('pre').code
    # @TODO: handle validating against this
    # @TODO: handle getting answer for part 2
    # answer = soup.find_all('code')[:-1]
    txt = input_.get_text()
    if not os.path.exists(TESTS_PATH):
        os.mkdir(TESTS_PATH)
    with open(f'{TESTS_PATH}{day}.txt', 'w') as out:
        out.write(txt)
    return txt


def print_grid(grid: Iterable[Iterable], spacer='') -> None:
    for row in grid:
        print(spacer.join(str(i) for i in row))
