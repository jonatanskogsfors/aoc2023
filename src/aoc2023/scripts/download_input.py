import sys
from http import HTTPStatus
from pathlib import Path

import requests

COOKIE_PATH = Path("session.txt")
INPUT_DIR = Path("input")
ENDPOINT_PATTERN = "https://adventofcode.com/2023/day/{}/input"


def main():
    day = int(sys.argv[1])
    input_path = INPUT_DIR / f"input_{day}.txt"

    if input_path.exists():
        sys.exit(f"Input data for day {day} already downloaded.")

    cookie = COOKIE_PATH.read_text().strip()
    cookies = {"session": cookie}
    url = ENDPOINT_PATTERN.format(day)
    response = requests.get(url, cookies=cookies)
    if response.status_code == HTTPStatus.OK:
        INPUT_DIR.mkdir(exist_ok=True)
        print(f"Writing '{input_path}'")
        input_path.write_text(response.text)
    else:
        sys.exit(f"Failed to download input for day {day}:\n{response.text}")
