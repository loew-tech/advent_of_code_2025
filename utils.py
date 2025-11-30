from datetime import datetime
from http import HTTPStatus
import requests
from typing import List, Callable

from constants import ADVENT_URI


def read_input(
        day: int | str,
        delim: str = '\n',
        year: int | str = None,
        parse: Callable[[List[str] | str], any] = None
) -> any:
    year = year if year is not None else datetime.now().year
    with open('.env') as env_:
        session_id = env_.read().strip().split('\n')[0]
    response = requests.get(f'{ADVENT_URI}{year}/day/{day}/input',
                            cookies={'session': session_id})
    data = None
    if response.status_code == HTTPStatus.OK:
        data = response.text.strip().split(delim) if delim else response.text
    return data if parse is None else parse(data)
