from datetime import datetime
from http import HTTPStatus
import requests
from typing import List

from constants import ADVENT_URI


def read_input(day: int | str, delim='\n', year=None) -> List[str] | str:
    year = year if year is not None else datetime.now().year
    with open('.env') as env_:
        session_id = env_.read().strip().split('\n')[0]
    response = requests.get(f'{ADVENT_URI}{year}/day/{day}/input',
                            cookies={'session': session_id})
    if response.status_code == HTTPStatus.OK:
        return response.text.strip().split(delim) if delim else response.text
