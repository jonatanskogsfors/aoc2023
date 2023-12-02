import sys
from pathlib import Path

import requests


COOKIE_PATH = Path("session.txt")
INPUT_DIR = Path("input")
ENDPOINT_PATTERN = "https://adventofcode.com/2023/day/{}/input"

if __name__ == "__main__":
    day = int(sys.argv[1])
    input_path = INPUT_DIR / f"input_{day}.txt"

    if input_path.exists():
        print(f"Input data for day {day} already downloaded.")
        sys.exit()

    cookie = COOKIE_PATH.read_text().strip()
    cookies = {f"session": cookie}
    url = ENDPOINT_PATTERN.format(day)
    response = requests.get(url, cookies=cookies)
    if response.status_code == 200:
        INPUT_DIR.mkdir(exist_ok=True)
        input_path.write_text(response.text)
