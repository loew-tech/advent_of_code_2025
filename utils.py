from datetime import datetime
from http import HTTPStatus
import requests
from typing import List, Callable

from bs4 import BeautifulSoup

from constants import ADVENT_URI


def read_input(
        day: int | str,
        year: int | str = 2025,
        delim: str = '\n',
        parse: Callable[[str], any] = None
) -> List[any] | str | None:
    year = year if year is not None else datetime.now().year
    with open('.env') as env_:
        session_id = env_.read().strip().split('\n')[0]
    response = requests.get(f'{ADVENT_URI}{year}/day/{day}/input',
                            cookies={'session': session_id})
    if not response.status_code == HTTPStatus.OK or response.text is None:
        return None
    return _process_input(response.text, delim, parse)


def test_problem(
        day: int | str,
        year: int | str = 2025,
        # delim: str = '\n',
        # parse: Callable[[List[str] | str], any] = None
) -> any:
    problem = requests.get(f'{ADVENT_URI}{year}/day/{day}')
    soup = BeautifulSoup(problem.content, 'html.parser')
    input_, *_, answer = soup.find_all('code')
    print(input_, type(input_))
    # print(f' processed={_process_input(input_, delim, parse)}')
    print(answer)


def _process_input(
        text, delim: str,
        parse: Callable[[List[str] | str], any]
) -> any:
    data = text.strip().split(delim) if delim else text
    return data if parse is None else [parse(e) for e in data]
